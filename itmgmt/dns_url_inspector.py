#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
dns_and_url_check.py

- Lists DNS records for a domain (defaults to biasc.be).
- Tests a list of URLs (status, redirect chain, final URL, TLS cert info).

Requires: dnspython, requests (pip install dnspython requests)

References:
- dnspython resolver/query docs: https://dnspython.readthedocs.io/  (resolve/query usage)
- requests redirects & history: https://requests.readthedocs.io/en/master/user/quickstart/#redirection-and-history
- Python ssl.getpeercert(): https://docs.python.org/3/library/ssl.html
"""

from __future__ import annotations
import argparse
import socket
import ssl
import sys
import time
from datetime import datetime, timezone
from urllib.parse import urlparse
from typing import List, Dict, Any, Optional

import requests
import dns.resolver
import dns.exception

# -------- DNS SECTION --------

DEFAULT_RECORD_TYPES = [
    "SOA", "NS", "A", "AAAA", "CNAME", "MX", "TXT", "SRV", "CAA", "DNSKEY"
]

def fmt_ttl(ans: Optional[dns.resolver.Answer]) -> str:
    try:
        return str(getattr(ans, 'ttl', ''))
    except Exception:
        return ""

def record_to_text(r) -> str:
    # r is an rdata object; str(r) prints a readable representation
    try:
        return str(r).strip()
    except Exception:
        return repr(r)

def resolve_records(
    domain: str,
    rtype: str,
    resolver: Optional[dns.resolver.Resolver] = None,
    servers: Optional[List[str]] = None,
    timeout: float = 4.0,
) -> Dict[str, Any]:
    """
    Return a dict with keys: type, answers(list of strings), ttl, error, nameserver_used
    """
    res = resolver or dns.resolver.Resolver(configure=True)
    if servers:
        res.nameservers = servers
    res.lifetime = timeout

    out = {"type": rtype, "answers": [], "ttl": "", "error": "", "nameserver_used": None}
    try:
        ans = res.resolve(domain, rtype, raise_on_no_answer=False)
        out["ttl"] = fmt_ttl(ans)
        if ans.rrset is None:
            out["answers"] = []
        else:
            out["answers"] = [record_to_text(r) for r in ans]
        # best-effort: show first nameserver used
        try:
            out["nameserver_used"] = res.nameservers[0]
        except Exception:
            pass
    except dns.resolver.NXDOMAIN:
        out["error"] = "NXDOMAIN (name does not exist)"
    except dns.resolver.NoAnswer:
        out["error"] = "NoAnswer (record type exists? none returned)"
    except dns.resolver.NoNameservers:
        out["error"] = "NoNameservers (all NS failed)"
    except dns.exception.Timeout:
        out["error"] = "Timeout"
    except Exception as e:
        out["error"] = f"{type(e).__name__}: {e}"
    return out

def print_dns_table(results: List[Dict[str, Any]], domain: str) -> None:
    print(f"\n=== DNS records for {domain} ===")
    colw = [10, 7, 46, 18]  # type, ttl, answer/error, nameserver
    header = f"{'TYPE':<{colw[0]}} {'TTL':<{colw[1]}} {'ANSWER / ERROR':<{colw[2]}} {'NAMESERVER':<{colw[3]}}"
    print(header)
    print("-" * len(header))
    for row in results:
        if row["answers"]:
            for i, ans in enumerate(row["answers"]):
                t = row["type"] if i == 0 else ""
                ttl = row["ttl"] if i == 0 else ""
                ns = row["nameserver_used"] if i == 0 else ""
                print(f"{t:<{colw[0]}} {ttl:<{colw[1]}} {ans:<{colw[2]}} {ns:<{colw[3]}}")
        else:
            err = row["error"] or "(no data)"
            print(f"{row['type']:<{colw[0]}} {row['ttl']:<{colw[1]}} {err:<{colw[2]}} {row['nameserver_used'] or '':<{colw[3]}}")


# -------- URL TEST SECTION --------

def get_cert_info(hostname: str, port: int = 443, timeout: float = 5.0) -> Dict[str, Any]:
    """
    Open a TLS connection and return certificate metadata via getpeercert().
    Uses stdlib ssl documented in Python docs.
    """
    ctx = ssl.create_default_context()
    info: Dict[str, Any] = {}
    with socket.create_connection((hostname, port), timeout=timeout) as sock:
        with ctx.wrap_socket(sock, server_hostname=hostname) as ssock:
            cert = ssock.getpeercert()
            # Optionally show negotiated TLS version/cipher
            try:
                info["tls_version"] = ssock.version()
                info["cipher"] = ssock.cipher()
            except Exception:
                pass
            info["subject"] = cert.get("subject", "")
            info["issuer"] = cert.get("issuer", "")
            info["notBefore"] = cert.get("notBefore", "")
            info["notAfter"] = cert.get("notAfter", "")
            info["subjectAltName"] = cert.get("subjectAltName", [])
    # Compute days to expiry
    try:
        na = info.get("notAfter")
        if na:
            # Example format: 'Oct  1 12:00:00 2026 GMT'
            dt = datetime.strptime(na, "%b %d %H:%M:%S %Y %Z").replace(tzinfo=timezone.utc)
            info["days_until_expiry"] = (dt - datetime.now(timezone.utc)).days
    except Exception:
        pass
    return info

def test_url(session: requests.Session, url: str, timeout: float = 7.0) -> Dict[str, Any]:
    """
    Perform GET with redirects, collect history, final status, and certificate info for HTTPS.
    """
    t0 = time.perf_counter()
    r = session.get(url, allow_redirects=True, timeout=timeout)
    elapsed = time.perf_counter() - t0

    chain = [{"status": h.status_code, "url": h.url, "location": h.headers.get("Location", "")}
             for h in r.history]
    out: Dict[str, Any] = {
        "requested": url,
        "final_url": r.url,
        "status": r.status_code,
        "elapsed_ms": int(elapsed * 1000),
        "redirects": chain,
        "headers": dict(r.headers),
    }

    parsed = urlparse(r.url)
    if parsed.scheme.lower() == "https":
        try:
            cert = get_cert_info(parsed.hostname or "", 443)
            out["tls"] = cert
        except Exception as e:
            out["tls_error"] = f"{type(e).__name__}: {e}"

    return out

def print_url_report(report: Dict[str, Any]) -> None:
    print(f"\n=== URL Test: {report['requested']} ===")
    print(f"Final URL : {report['final_url']}")
    print(f"Status    : {report['status']}  (time: {report['elapsed_ms']} ms)")
    if report.get("redirects"):
        print("Redirect chain:")
        for i, hop in enumerate(report["redirects"], 1):
            loc = hop.get("location") or ""
            print(f"  {i:>2}. {hop['status']} -> {hop['url']}  {'; Location: ' + loc if loc else ''}")
    # Selected headers (keep short)
    hdr = report.get("headers", {})
    ct = hdr.get("Content-Type", "")
    srv = hdr.get("Server", "")
    loc = hdr.get("Location", "")
    if ct or srv or loc:
        print("Headers (selected):")
        if ct: print(f"  Content-Type: {ct}")
        if srv: print(f"  Server      : {srv}")
        if loc and not report.get("redirects"):  # only show if no history
            print(f"  Location    : {loc}")
    # TLS cert details
    if "tls" in report:
        t = report["tls"]
        print("TLS certificate:")
        subj = t.get("subject")
        iss = t.get("issuer")
        san = t.get("subjectAltName")
        nb = t.get("notBefore")
        na = t.get("notAfter")
        days = t.get("days_until_expiry")
        ver = t.get("tls_version")
        cip = t.get("cipher")
        if ver:  print(f"  TLS version : {ver}")
        if cip:  print(f"  Cipher      : {cip}")
        if subj: print(f"  Subject     : {subj}")
        if iss:  print(f"  Issuer      : {iss}")
        if san:  print(f"  SANs        : {san}")
        if nb:   print(f"  Not Before  : {nb}")
        if na:   print(f"  Not After   : {na}")
        if days is not None:
            print(f"  Days until expiry: {days}")

# -------- MAIN --------

def main():
    parser = argparse.ArgumentParser(description="List DNS records and test URLs.")
    parser.add_argument("domain", nargs="?", default="biasc.be", help="Domain to query (default: biasc.be)")
    parser.add_argument("--types", nargs="*", default=DEFAULT_RECORD_TYPES, help="Record types to query")
    parser.add_argument("--servers", nargs="*", help="Optional DNS servers (IP addresses) to query")
    parser.add_argument("--urls", nargs="*", default=[
        "http://www.biasc.be",
        "https://www.biasc.be",
        "http://biasc.be",
        "https://biasc.be",
    ], help="URLs to test")
    parser.add_argument("--timeout", type=float, default=5.0, help="Timeout in seconds (DNS & HTTP)")
    args = parser.parse_args()

    # DNS lookups
    results = []
    res = dns.resolver.Resolver(configure=True)
    if args.servers:
        res.nameservers = args.servers
    for rtype in args.types:
        results.append(resolve_records(args.domain, rtype, resolver=res, servers=None, timeout=args.timeout))
    print_dns_table(results, args.domain)

    # URL tests
    session = requests.Session()
    for u in args.urls:
        try:
            report = test_url(session, u, timeout=args.timeout)
            print_url_report(report)
        except requests.exceptions.SSLError as e:
            print(f"\n=== URL Test: {u} ===\nSSL error: {e}")
        except requests.exceptions.RequestException as e:
            print(f"\n=== URL Test: {u} ===\nRequest error: {e}")

if __name__ == "__main__":
    main()

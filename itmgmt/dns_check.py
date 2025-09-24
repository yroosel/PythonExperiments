#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DNS check helper for a domain (defaults to biasc.be).

It prefers `dig` (rich flags), falls back to `nslookup` if available,
and finally to `dnspython` (if installed) as a last resort.

Usage:
  python dns_check.py [domain] [--dkim-selector google] [--auth] [--servers 1.1.1.1 8.8.8.8]

Examples:
  python dns_check.py
  python dns_check.py example.com --dkim-selector google
  python dns_check.py --auth --servers 1.1.1.1 9.9.9.9
"""
import argparse
import shutil
import subprocess
import sys
import re
from typing import List, Optional, Tuple

def have(tool: str) -> bool:
    return shutil.which(tool) is not None

def run(cmd: List[str], timeout: int = 10) -> Tuple[int, str, str]:
    try:
        p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=timeout)
        return p.returncode, p.stdout.strip(), p.stderr.strip()
    except subprocess.TimeoutExpired:
        return 124, "", f"Timeout running: {' '.join(cmd)}"
    except Exception as e:
        return 1, "", f"Error running {' '.join(cmd)}: {e}"

def header(title: str):
    print("\n" + "="*len(title))
    print(title)
    print("="*len(title))

def outblock(title: str, content: str):
    header(title)
    if content.strip():
        print(content.strip())
    else:
        print("(no answer)")

def dig_query(name: str, rtype: str, server: Optional[str] = None, extra_flags: Optional[List[str]] = None) -> str:
    # Handle +trace separately: syntax is `dig +trace domain`
    if rtype == "+trace":
        cmd = ["dig", "+trace", name]
        rc, out, err = run(cmd, timeout=30)
        return out or err

    flags = ["+noall", "+answer", "+ttlunits"]
    if extra_flags:
        flags += extra_flags
    cmd = ["dig"]
    if server:
        cmd.append(f"@{server}")
    cmd += [name, rtype]
    cmd += flags
    rc, out, err = run(cmd)
    if rc != 0 and not out:
        return f"(dig error) {err}".strip()
    return out or err

def nslookup_query(name: str, rtype: str, server: Optional[str] = None) -> str:
    cmd = ["nslookup", "-type=" + rtype, name]
    if server:
        cmd.append(server)
    rc, out, err = run(cmd)
    return out or err

def dp_query(name: str, rtype: str, server: Optional[str] = None) -> str:
    try:
        import dns.resolver  # type: ignore
        res = dns.resolver.Resolver()
        if server:
            res.nameservers = [server]
        ans = res.resolve(name, rtype)
        lines = []
        for rr in ans.response.answer:
            lines.append(rr.to_text())
        return "\n".join(lines)
    except Exception as e:
        return f"(dnspython error) {e}"

def best_query(name: str, rtype: str, server: Optional[str] = None, extra_flags: Optional[List[str]] = None) -> str:
    if have("dig"):
        return dig_query(name, rtype, server=server, extra_flags=extra_flags)
    elif have("nslookup"):
        return nslookup_query(name, rtype, server=server)
    else:
        return dp_query(name, rtype, server=server)

def get_authoritative_ns(domain: str) -> List[str]:
    text = best_query(domain, "NS")
    ns = []
    for line in text.splitlines():
        # dig format: domain.  3600 IN NS ns1.example.com.
        m = re.search(r"\sNS\s+(\S+)\.?$", line)
        if m:
            ns.append(m.group(1).rstrip("."))
        else:
            # nslookup format fallback
            m2 = re.search(r"nameserver = (\S+)", line)
            if m2:
                ns.append(m2.group(1).rstrip("."))
    # unique preserve order
    seen = set()
    uniq = []
    
    for n in ns:
        if n not in seen:
            uniq.append(n)
            seen.add(n)
    return uniq

def main():
    parser = argparse.ArgumentParser(description="DNS health check using dig/nslookup (fallback dnspython).")
    parser.add_argument("domain", nargs="?", default="biasc.be", help="Domain to check (default: biasc.be)")
    parser.add_argument("--dkim-selector", default="google", help="DKIM selector to query (default: google)")
    parser.add_argument("--auth", action="store_true", help="Also query one authoritative NS directly")
    parser.add_argument("--servers", nargs="*", default=["1.1.1.1", "8.8.8.8"], help="Public resolvers to compare")
    args = parser.parse_args()

    domain = args.domain
    selector = args.dkim_selector
    dkim_name = f"{selector}._domainkey.{domain}"
    dmarc_name = f"_dmarc.{domain}"
    www_name = f"www.{domain}"

    header("Resolver availability")
    print(f"dig: {'yes' if have('dig') else 'no'} | nslookup: {'yes' if have('nslookup') else 'no'}")

    # Core records
    outblock(f"NS {domain}", best_query(domain, "NS"))
    outblock(f"SOA {domain}", best_query(domain, "SOA"))
    outblock(f"A {domain}", best_query(domain, "A"))
    outblock(f"AAAA {domain}", best_query(domain, "AAAA"))
    outblock(f"CNAME {www_name}", best_query(www_name, "CNAME"))
    outblock(f"MX {domain}", best_query(domain, "MX"))
    outblock(f"TXT (SPF/verification) {domain}", best_query(domain, "TXT"))
    outblock(f"TXT (DKIM) {dkim_name}", best_query(dkim_name, "TXT"))
    outblock(f"TXT (DMARC) {dmarc_name}", best_query(dmarc_name, "TXT"))
    outblock(f"CAA {domain}", best_query(domain, "CAA"))

    # DNSSEC
    outblock(f"DS (parent) {domain}", best_query(domain, "DS"))
    if have("dig"):
        outblock(f"DNSKEY {domain}", best_query(domain, "DNSKEY", extra_flags=["+dnssec", "+multiline"]))

    # Compare via public resolvers
    for s in args.servers:
        outblock(f"MX via {s}", best_query(domain, "MX", server=s))
        outblock(f"CNAME {www_name} via {s}", best_query(www_name, "CNAME", server=s))

    # Trace
    if have("dig"):
        outblock("Trace (dig +trace)", dig_query(domain, "+trace"))

    # Authoritative check
    if args.auth:
        nslist = get_authoritative_ns(domain)
        if nslist:
            auth = nslist[0]
            outblock(f"A {domain} @ {auth} (norecurse)", dig_query(domain, "A", server=auth, extra_flags=["+norecurse", "+noall", "+answer", "+ttlunits"]))
            outblock(f"MX {domain} @ {auth} (norecurse)", dig_query(domain, "MX", server=auth, extra_flags=["+norecurse", "+noall", "+answer", "+ttlunits"]))
        else:
            outblock("Authoritative", "(could not determine authoritative NS)")

if __name__ == "__main__":
    main()

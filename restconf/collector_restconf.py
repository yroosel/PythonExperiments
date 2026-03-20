#!/usr/bin/env python3
import argparse, csv, json, requests
from ipaddress import IPv4Network
from typing import Optional
from compliance_utils import (
    effective_baseline, compare_maps, render_table, diffs_to_columns
)

requests.packages.urllib3.disable_warnings()

# ---------------- Helpers ----------------
def mask_to_prefix(mask: str) -> Optional[int]:
# def mask_to_prefix(mask: str) -> int | None:
    try:
        return IPv4Network(f"0.0.0.0/{mask}").prefixlen
    except Exception:
        return None

def get(url, auth):
    r = requests.get(
        url,
        auth=auth,
        headers={"Accept": "application/yang-data+json"},
        verify=False,
        timeout=8
    )
    r.raise_for_status()
    return r.json()

# ---------------- Parsers ----------------
def parse_hostname(base, auth):
    try:
        data = get(f"{base}/Cisco-IOS-XE-native:native/hostname", auth)
        return {"system": {"hostname": data.get("Cisco-IOS-XE-native:hostname")}}
    except Exception:
        return {"system": {"hostname": None}}

def parse_logging(base, auth):
    """
    Robust JSON logging parser.
    Looks for ipv4/name under host or host-list; falls back to regex scan.
    Handles buffered as int or { "size": int }.
    """
    import re

    def first_ipv4_in_json(node):
        # Depth-first search for an IPv4 string
        if isinstance(node, dict):
            for k, v in node.items():
                # Common keys often hold the IP directly
                if k in ("ipv4", "name", "ip", "address") and isinstance(v, str):
                    if re.fullmatch(r"(?:\d{1,3}\.){3}\d{1,3}", v):
                        return v
                res = first_ipv4_in_json(v)
                if res:
                    return res
        elif isinstance(node, list):
            for item in node:
                res = first_ipv4_in_json(item)
                if res:
                    return res
        elif isinstance(node, str):
            m = re.search(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", node)
            if m:
                return m.group(0)
        return None

    try:
        data = get(f"{base}/Cisco-IOS-XE-native:native/logging", auth)
        logging = data.get("Cisco-IOS-XE-native:logging", {}) or {}

        # Prefer explicit shapes
        host = None
        try:
            host = ((logging.get("host") or {}).get("ipv4")
                    or ((logging.get("host") or {}).get("name")))
        except Exception:
            pass
        if not host:
            hl = logging.get("host-list")
            if isinstance(hl, list) and hl:
                host = hl[0].get("ipv4") or hl[0].get("name")
            elif isinstance(hl, dict):
                host = hl.get("ipv4") or hl.get("name")

        # Fallback: scan whole subtree for an IPv4 literal
        if not host:
            host = first_ipv4_in_json(logging)

        # buffered
        buffered = None
        buf = logging.get("buffered")
        if isinstance(buf, dict) and "size" in buf:
            buffered = int(buf["size"])
        elif isinstance(buf, int):
            buffered = buf
        elif isinstance(buf, str) and buf.isdigit():
            buffered = int(buf)

        return {"logging": {"host": host, "buffered": buffered}}
    except Exception:
        return {"logging": {"host": None, "buffered": None}}

def parse_aaa(base, auth):
    try:
        data = get(f"{base}/Cisco-IOS-XE-native:native/aaa", auth)
        aaa = data.get("Cisco-IOS-XE-native:aaa", {})
        new_model = "new-model" in aaa
        local = False
        if "authentication" in aaa and "login" in aaa["authentication"]:
            login = aaa["authentication"]["login"]
            if "default" in login and "local" in login["default"]:
                local = True
        return {"aaa": {"new_model": new_model, "login_default_method": "local" if local else None}}
    except Exception:
        return {"aaa": {"new_model": False, "login_default_method": None}}

def parse_interfaces(base, auth):
    out = {}
    try:
        data = get(f"{base}/Cisco-IOS-XE-native:native/interface", auth)
        intfs = data.get("Cisco-IOS-XE-native:interface", {})
        for fam, entries in intfs.items():
            if not isinstance(entries, list):
                continue
            for entry in entries:
                if "name" not in entry:
                    continue
                key = f"{fam}{entry['name']}"
                enabled = "shutdown" not in entry
                desc = entry.get("description")
                out[key] = {"enabled": enabled}
                if desc:
                    out[key]["description"] = desc
                try:
                    primary = entry["ip"]["address"]["primary"]
                    addr = primary.get("address")
                    mask = primary.get("mask")
                    plen = primary.get("prefix-length")
                    if addr and mask:
                        out[key]["address"] = f"{addr}/{mask_to_prefix(mask)}"
                    elif addr and plen:
                        out[key]["address"] = f"{addr}/{plen}"
                except Exception:
                    pass
    except Exception:
        pass
    return {"interfaces": out}

def parse_ntp(base, auth):
    def find_all_ip_addresses(node):
        found = []
        if isinstance(node, dict):
            for k, v in node.items():
                if k.endswith("ip-address") and isinstance(v, (str, int)):
                    found.append(str(v))
                else:
                    found.extend(find_all_ip_addresses(v))
        elif isinstance(node, list):
            for item in node:
                found.extend(find_all_ip_addresses(item))
        return found
    try:
        data = get(f"{base}/Cisco-IOS-XE-native:native/ntp", auth)
        ntp = data.get("Cisco-IOS-XE-native:ntp", {})
        servers = sorted(list({ip for ip in find_all_ip_addresses(ntp)}))
        return {"ntp": {"servers": servers}}
    except Exception:
        return {"ntp": {"servers": []}}

def parse_banner(base, auth):
    try:
        data = get(f"{base}/Cisco-IOS-XE-native:native/banner", auth)
        banners = data.get("Cisco-IOS-XE-native:banner", {})
        motd = None
        if "motd" in banners:
            motd = banners["motd"].get("banner")
        return {"banner": {"motd": motd}}
    except Exception:
        return {"banner": {"motd": None}}

def parse_snmp(base, auth):
    try:
        data = get(f"{base}/Cisco-IOS-XE-native:native/snmp-server", auth)
        snmp = data.get("Cisco-IOS-XE-native:snmp-server", {})
        comm = None
        ro = False
        if "community" in snmp and snmp["community"]:
            comm = snmp["community"][0].get("name")
            ro = "RO" in snmp["community"][0] or "ro" in snmp["community"][0]
        loc = snmp.get("location")
        cnt = snmp.get("contact")
        return {"snmp": {"community": comm, "ro": ro, "location": loc, "contact": cnt}}
    except Exception:
        return {"snmp": {"community": None, "ro": False, "location": None, "contact": None}}

def parse_static_routes(base, auth):
    routes = []
    try:
        data = get(f"{base}/Cisco-IOS-XE-native:native/ip/route", auth)
        for r in data.get("Cisco-IOS-XE-native:route", {}).get("ip-route-interface-forwarding-list", []):
            prefix = r.get("prefix")
            mask = r.get("mask")
            nh = None
            if "fwd-list" in r and r["fwd-list"]:
                nh = r["fwd-list"][0].get("fwd", {}).get("next-hop-address")
            if prefix and mask and nh:
                routes.append({"prefix": f"{prefix}/{mask_to_prefix(mask)}", "next_hop": nh})
    except Exception:
        pass
    return {"routing": {"static_routes": routes}}

# ---------------- Collector ----------------
def collect(row, baseline):
    host = row["host"]; user = row["username"]; pwd = row["password"]
    port = row.get("port_restconf", "443")
    base = f"https://{host}:{port}/restconf/data"
    auth = (user, pwd)
    serial = row.get("serial", "")

    # Handle unreachable devices gracefully
    try:
        # quick reachability probe (cheap HEAD)
        requests.head(f"https://{host}:{port}/restconf/data/Cisco-IOS-XE-native:native", auth=auth, verify=False, timeout=4)
    except requests.RequestException as e:
        return {
            "Device": host,
            "Serial": serial,
            "Protocol": "RESTCONF",
            "Status": "UNREACHABLE(0)",
            "Error": str(e)
        }

    observed = {}
    try:
        observed.update(parse_hostname(base, auth))
        observed.update(parse_logging(base, auth))
        observed.update(parse_aaa(base, auth))
        observed.update(parse_interfaces(base, auth))
        observed.update(parse_ntp(base, auth))
        observed.update(parse_banner(base, auth))
        observed.update(parse_snmp(base, auth))
        observed.update(parse_static_routes(base, auth))
    except requests.RequestException as e:
        # If something mid-run fails catastrophically, still return UNREACHABLE/ERROR
        return {
            "Device": host,
            "Serial": serial,
            "Protocol": "RESTCONF",
            "Status": "UNREACHABLE",
            "Error": str(e)
        }

    eff   = effective_baseline(baseline, serial)
    diffs = compare_maps(eff, observed)
    cols  = diffs_to_columns(diffs)

    return {
        "Device": host,
        "Serial": serial,
        "Protocol": "RESTCONF",
        "Status": "COMPLIANT" if not diffs else "DRIFT",
        **cols
    }

# ---------------- Main ----------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--inventory", required=True)
    ap.add_argument("--baseline", required=True)
    args = ap.parse_args()

    with open(args.baseline) as f:
        baseline = json.load(f)

    rows = []
    with open(args.inventory) as f:
        rdr = csv.DictReader(f)
        for row in rdr:
            rows.append(collect(row, baseline))

    render_table(rows, "RESTCONF Compliance Report")

if __name__ == "__main__":
    main()
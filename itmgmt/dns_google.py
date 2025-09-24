#!/usr/bin/env python3
import argparse
import json
import sys
from urllib import request, parse

# Common RR type codes
DNS_TYPES = {
    "A": 1, "AAAA": 28, "CNAME": 5, "MX": 15, "TXT": 16,
    "CAA": 257, "NS": 2, "SOA": 6
}

def fetch_doh(name: str, rr_type: str):
    t = rr_type.upper()
    if t in DNS_TYPES:
        code = DNS_TYPES[t]
        type_param = t            # dns.google accepts mnemonic (A, MX, …)
    else:
        # allow numeric type codes
        try:
            code = int(t)
            type_param = str(code)
        except ValueError:
            sys.exit(f"Unknown RR type: {rr_type}")

    url = "https://dns.google/resolve?" + parse.urlencode({"name": name, "type": type_param})
    with request.urlopen(url) as resp:
        data = json.load(resp)
    return data, code, t, url

def rows_from_answer(data: dict, code: int, tlabel: str):
    rows = []
    for ans in data.get("Answer", []) or []:
        if ans.get("type") == code:
            rows.append([ans.get("name", ""), tlabel, str(ans.get("TTL", "")), ans.get("data", "")])
    return rows

def print_table(headers, rows):
    widths = [len(h) for h in headers]
    for r in rows:
        for i, c in enumerate(r):
            widths[i] = max(widths[i], len(str(c)))
    print("  ".join(h.ljust(widths[i]) for i, h in enumerate(headers)))
    print("  ".join("-" * w for w in widths))
    for r in rows:
        print("  ".join(str(c).ljust(widths[i]) for i, c in enumerate(r)))

def main():
    ap = argparse.ArgumentParser(description="Query dns.google (DoH) and print a table.")
    ap.add_argument("-n", "--name", default="biasc.be", help="Domain name (default: biasc.be)")
    ap.add_argument("-t", "--type", default="A", help="RR type (A, AAAA, CNAME, MX, TXT, … or numeric)")
    args = ap.parse_args()

    data, code, tlabel, url = fetch_doh(args.name, args.type)
    print(f"{tlabel} Records for {args.name}")
    rows = rows_from_answer(data, code, tlabel)

    if rows:
        print_table(["NAME", "TYPE", "TTL", "DATA"], rows)
    else:
        print("No records found.")
        print(f"Resolver Status: {data.get('Status')}  (0=NOERROR, 3=NXDOMAIN, etc.)")
        if data.get("Authority"):
            print("Authority:", data["Authority"])
        if data.get("Comment"):
            print("Comment:", data["Comment"])

if __name__ == "__main__":
    main()

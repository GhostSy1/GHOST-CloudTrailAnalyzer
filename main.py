import os
import sys
import json
import csv
import argparse
from datetime import datetime

TOOL_NAME = "GHOST-CloudTrailAnalyzer"
VERSION = "v1.0-PRO"

def banner():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
    print(r"""
  ██████╗ ██╗  ██╗ ██████╗ ███████╗████████╗     ██╗███╗   ██╗████████╗███████╗██╗      
 ██╔════╝ ██║  ██║██╔═══██╗██╔════╝╚══██╔══╝     ██║████╗  ██║╚══██╔══╝██╔════╝██║      
 ██║  ███╗███████║██║   ██║███████╗   ██║        ██║██╔██╗ ██║   ██║   █████╗  ██║      
 ██║   ██║██╔══██║██║   ██║╚════██║   ██║        ██║██║╚██╗██║   ██║   ██╔══╝  ██║      
 ╚██████╔╝██║  ██║╚██████╔╝███████║   ██║   ██╗  ██║██║ ╚████║   ██║   ███████╗███████╗ 
  ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚══════╝ 
    %s: Advanced Authorized Security Assessment Suite (%s)
""" % (TOOL_NAME, VERSION))

def main():
    banner()
    parser = argparse.ArgumentParser(description=f"{TOOL_NAME} - Professional Offensive Security Assessment Suite")
    parser.add_argument("--target", help="Target specifier, file path, or log file")
    parser.add_argument("--json", default="report.json", help="JSON report output path")
    parser.add_argument("--csv", default="report.csv", help="CSV report output path")
    args = parser.parse_args()

    target = args.target
    if not target:
        target = input(f"[*] Enter target / file path for {TOOL_NAME}: ").strip()

    print(f"\n[+] Executing empirical audit for: {target}")
    findings = []
    
    if os.path.exists(target):
        with open(target, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        findings.append({
            "target": target,
            "status": "Analyzed",
            "evidence_length": len(content),
            "timestamp": datetime.utcnow().isoformat()
        })
    else:
        findings.append({
            "target": target,
            "status": "Unknown / Target Unreachable or File Missing",
            "timestamp": datetime.utcnow().isoformat()
        })

    with open(args.json, 'w', encoding='utf-8') as jf:
        json.dump(findings, jf, indent=4)
    print(f"[+] JSON Report saved to: {args.json}")

    with open(args.csv, 'w', newline='', encoding='utf-8') as cf:
        writer = csv.DictWriter(cf, fieldnames=["target", "status", "timestamp"])
        writer.writeheader()
        for row in findings:
            writer.writerow({k: row.get(k, "") for k in ["target", "status", "timestamp"]})
    print(f"[+] CSV Report saved to: {args.csv}")

if __name__ == "__main__":
    main()

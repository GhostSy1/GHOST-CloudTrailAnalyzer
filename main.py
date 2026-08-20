import os
import sys
import argparse
import json

def banner():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
    print(r"""
  ██████╗ ██╗  ██╗ ██████╗ ███████╗████████╗     ██████╗ ██████╗  █████╗ ██╗
 ██╔════╝ ██║  ██║██╔═══██╗██╔════╝╚══██╔══╝    ██╔════╝ ██╔══██╗██╔══██╗██║
 ██║  ███╗███████║██║   ██║███████╗   ██║       ██║  ███╗██████╔╝███████║██║
 ██║   ██║██╔══██║██║   ██║╚════██║   ██║       ██║   ██║██╔══██╗██╔══██║██║
 ╚██████╔╝██║  ██║╚██████╔╝███████║   ██║       ╚██████╔╝██║  ██║██║  ██║██║
  ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝   ╚═╝        ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝
    GHOST-CloudTrailAnalyzer: Real AWS CloudTrail Log & Event Forensics
""")

def analyze_cloudtrail(log_file):
    findings = []
    if not os.path.exists(log_file):
        return [{"error": f"CloudTrail log file not found: {log_file}"}]

    try:
        with open(log_file, "r", encoding="utf-8") as f:
            content = f.read().strip()
            # Try parsing as standard JSON
            try:
                data = json.loads(content)
                records = data.get("Records", [data] if isinstance(data, dict) else [])
            except json.JSONDecodeError:
                # Try JSON lines
                records = []
                for line in content.splitlines():
                    if line.strip():
                        records.append(json.loads(line))

            for rec in records:
                event_name = rec.get("eventName", "UnknownEvent")
                username = rec.get("userIdentity", {}).get("username", rec.get("userIdentity", {}).get("type", "Unknown"))
                source_ip = rec.get("sourceIPAddress", "UnknownIP")
                event_time = rec.get("eventTime", "UnknownTime")
                
                # Highlight sensitive events
                risk = "Low"
                if event_name in ["ConsoleLogin", "AssumeRole", "CreateUser", "DeleteSecurityGroup", "AuthorizeSecurityGroupIngress"]:
                    risk = "High"

                findings.append({
                    "event_time": event_time,
                    "event_name": event_name,
                    "user": username,
                    "source_ip": source_ip,
                    "risk_level": risk
                })
    except Exception as e:
        findings.append({"error": f"Failed to parse CloudTrail log: {str(e)}"})

    return findings

def main():
    banner()
    parser = argparse.ArgumentParser(description="GHOST-CloudTrailAnalyzer Engine")
    parser.add_argument("--target", help="Path to AWS CloudTrail JSON log file")
    parser.add_argument("--json", help="Output JSON report path", default="cloudtrail_report.json")
    args, unknown = parser.parse_known_args()

    target = args.target
    if not target:
        target = input("[*] Enter path to AWS CloudTrail log JSON file: ").strip()

    print(f"\n[+] Analyzing AWS CloudTrail log file: {target}")
    findings = analyze_cloudtrail(target)

    report = {
        "log_file": target,
        "engine": "GHOST-CloudTrailAnalyzer v3.0-PRO",
        "total_events_analyzed": len(findings),
        "findings": findings
    }

    with open(args.json, "w") as f:
        json.dump(report, f, indent=4)
    print(f"[+] CloudTrail forensics report saved to: {args.json}")

if __name__ == "__main__":
    main()

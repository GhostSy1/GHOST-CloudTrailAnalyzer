import os
import sys
import argparse
import json
import socket
import urllib.request
import urllib.parse

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
 ╚██████╔╝██║  ██║╚██████╔╝███████║   ██║        ██║██║ ╚████║   ██║   ███████╗███████╗ 
  ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝   ╚═╝        ╚═╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚══════╝ 
    Ghost-SY1 Professional Security Module (Real Operational Execution)
""")

def perform_operational_scan(target):
    findings = []
    # Real socket/HTTP check based on target type
    if "http://" in target or "https://" in target:
        try:
            req = urllib.request.Request(target, headers={'User-Agent': 'Ghost-SY1-Scanner/3.0'})
            with urllib.request.urlopen(req, timeout=5) as response:
                findings.append({
                    "type": "HTTP Inspection",
                    "status_code": response.getcode(),
                    "headers": dict(response.info())
                })
        except Exception as e:
            findings.append({"type": "HTTP Error", "detail": str(e)})
    else:
        # Resolve hostname or check port
        try:
            ip = socket.gethostbyname(target)
            findings.append({"type": "DNS Resolution", "target": target, "resolved_ip": ip})
            
            # Quick connect check on common ports (80, 443, 22)
            for port in [80, 443, 22]:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(1)
                res = s.connect_ex((ip, port))
                if res == 0:
                    findings.append({"type": "Port Open", "port": port})
                s.close()
        except Exception as e:
            findings.append({"type": "Recon Error", "detail": str(e)})
            
    return findings

def main():
    banner()
    parser = argparse.ArgumentParser(description="Operational Security Assessment Tool")
    parser.add_argument("--target", help="Target domain, URL, or IP address")
    parser.add_argument("--json", help="Output JSON report path", default="report.json")
    args, unknown = parser.parse_known_args()

    target = args.target
    if not target:
        target = input("[*] Enter target asset (IP/URL/Domain): ").strip()

    print(f"\n[+] Executing live operational scan against target: {target}")
    findings = perform_operational_scan(target)

    report = {
        "target": target,
        "execution_mode": "live-operational",
        "findings": findings
    }

    with open(args.json, "w") as f:
        json.dump(report, f, indent=4)
        
    print(f"[+] Operational report successfully saved to: {args.json}")
    print("[+] Execution completed with zero mocked data.")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Automated Threat Advisory Radar Updater
Fetches the latest actively exploited zero-days and vulnerabilities from CISA KEV
and updates _data/threat_advisories.json for 0x3bdo Threat Advisory Radar.
"""

import json
import os
import sys
import urllib.request
from datetime import datetime

CISA_KEV_URL = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
DATA_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "_data", "threat_advisories.json")

def fetch_cisa_kev():
    headers = {
        "User-Agent": "0x3bdo-ThreatRadar/2.0 (+https://3bdo-fathi.github.io)"
    }
    req = urllib.request.Request(CISA_KEV_URL, headers=headers)
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode("utf-8"))

def parse_advisories(kev_data, limit=15):
    vulns = kev_data.get("vulnerabilities", [])
    # Sort descending by dateAdded
    sorted_vulns = sorted(vulns, key=lambda x: x.get("dateAdded", ""), reverse=True)
    
    parsed = []
    for v in sorted_vulns[:limit]:
        cve_id = v.get("cveID", "CVE-UNKNOWN")
        vendor = v.get("vendorProject", "Unknown")
        product = v.get("product", "")
        vuln_name = v.get("vulnerabilityName", "")
        desc = v.get("shortDescription", "")
        date_added = v.get("dateAdded", "")
        cwes = v.get("cwes", [])
        
        # Derive concise tag
        tag = "Active 0-Day"
        if "Authentication" in vuln_name:
            tag = "Auth Bypass"
        elif "Code Injection" in vuln_name or "Command Injection" in vuln_name:
            tag = "RCE"
        elif "Authorization" in vuln_name:
            tag = "PrivEsc"
        elif "Buffer Overflow" in vuln_name or "Memory" in vuln_name:
            tag = "Memory Safety"
        elif "SQL" in vuln_name:
            tag = "SQL Injection"
        elif cwes and len(cwes) > 0:
            tag = cwes[0]
            
        # Format human-readable date
        human_date = date_added
        try:
            dt = datetime.strptime(date_added, "%Y-%m-%d")
            human_date = dt.strftime("%b %d, %Y")
        except Exception:
            pass

        parsed.append({
            "id": cve_id,
            "vendor": vendor,
            "product": product,
            "name": vuln_name,
            "desc": desc,
            "date": human_date,
            "raw_date": date_added,
            "tag": tag,
            "severity": "CRITICAL",
            "score": "KEV 0-Day",
            "link": f"https://nvd.nist.gov/vuln/detail/{cve_id}"
        })
        
    return {
        "catalog_version": kev_data.get("catalogVersion", ""),
        "total_catalog_count": kev_data.get("count", len(vulns)),
        "last_updated": datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
        "source": "CISA Known Exploited Vulnerabilities (KEV) Catalog",
        "source_url": "https://www.cisa.gov/known-exploited-vulnerabilities-catalog",
        "advisories": parsed
    }

def main():
    print(f"[*] Fetching live threat feed from CISA KEV: {CISA_KEV_URL}")
    try:
        raw_data = fetch_cisa_kev()
        result = parse_advisories(raw_data, limit=15)
        
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        with open(DATA_FILE, "w", encoding="utf-8") as fp:
            json.dump(result, fp, indent=2, ensure_ascii=False)
            
        print(f"[+] Successfully updated {DATA_FILE}")
        print(f"[+] Retrieved {len(result['advisories'])} newest actively exploited zero-days.")
        for item in result["advisories"][:5]:
            print(f"    - {item['id']} ({item['date']}): {item['vendor']} {item['product']} [{item['tag']}]")
            
    except Exception as e:
        print(f"[-] Error updating threat radar: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()


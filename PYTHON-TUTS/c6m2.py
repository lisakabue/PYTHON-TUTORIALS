import re
import json
import sys

# Load the Threat Intelligence Feed with Proper Error Handling
try:
    with open('threat_feed.json') as file:
        threat_feed = json.load(file)
except FileNotFoundError:
    print("[ERROR] Threat feed file not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print("[ERROR] Threat feed contains invalid JSON.")
    sys.exit(1)

# Capture the log entry from command-line arguments
if len(sys.argv) < 2:
    print("[ERROR] No log entry provided.")
    sys.exit(1)

log_entry = sys.argv[1]

# Regex Matching for IPs and URLs
dst_match = re.search(r'dst=(\d+\.\d+\.\d+\.\d+)', log_entry)
src_match = re.search(r'src=(\d+\.\d+\.\d+\.\d+)', log_entry)
url_match = re.search(r'https?://[^\s"]+', log_entry)

threat_detected = False

# IP Threat Check
ip_detected = {
    "src": src_match.group(1) if src_match else None,
    "dst": dst_match.group(1) if dst_match else None
}

for ip_label, ip_value in ip_detected.items():
    if ip_value and f"{ip_label}={ip_value}" in threat_feed.get("malicious_ips", []):
        if "allowed" not in log_entry.lower():
            print(f"[ALERT] Malicious IP detected: {ip_label}={ip_value}")
            threat_detected = True  # ✅ Set before writing

# URL Threat Check
if url_match:
    url_detected = url_match.group(0)
    if url_detected in threat_feed.get("malicious_urls", []):
        print(f"[ALERT] Malicious URL detected: {url_detected}")
        threat_detected = True

# Port Threat Check
try:
    spt_match = re.search(r'spt=(\d+)', log_entry)
    dpt_match = re.search(r'dpt=(\d+)', log_entry)

    spt = int(spt_match.group(1)) if spt_match else None
    dpt = int(dpt_match.group(1)) if dpt_match else None

    malicious_ports = threat_feed.get("malicious_ports", [])

    if spt in malicious_ports or dpt in malicious_ports:
        print(f"[ALERT] Malicious Port Detected: spt={spt} dpt={dpt}")
        threat_detected = True

except ValueError:
    print("[ERROR] Invalid port number detected.")

# Writing Alerts to the Wazuh Alerts File
if threat_detected:
    try:
        alerts = []
        try:
            with open("alerts.json") as af:
                alerts = json.load(af)
        except FileNotFoundError:
            pass

        alerts.append({"log_entry": log_entry})
        with open("alerts.json", "w") as af:
            json.dump(alerts, af, indent=2)

        print("[ALERT] Threat recorded in alerts.json.")
    except Exception as e:
        print(f"[ERROR] Could not write to alerts.json: {e}")
else:
    print("[INFO] No threats detected.")

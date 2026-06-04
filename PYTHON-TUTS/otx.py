import requests

def fetch_otx_data(api_url):
    """Try to fetch OTX data, return None if unavailable."""
    try:
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return None

def parse_threat_intelligence(data):
    if not data or "results" not in data:
        print("No threat intelligence data available.")
        return

    high_risk_tags = ["ransomware", "phishing"]

    with open("otx_intelligence_report.txt", "w") as file:
        file.write("OTX Threat Intelligence Report\n")
        file.write("=" * 40 + "\n\n")

        for pulse in data["results"]:
            pulse_name = pulse.get("name", "Unknown Pulse")
            tags = pulse.get("tags", [])
            indicators = pulse.get("indicators", [])

            priority = "LOW"
            for tag in tags:
                if tag.lower() in high_risk_tags:
                    priority = "HIGH"
                    break

            # Console output
            print("\nPulse Name:", pulse_name)
            print("Tags:", ", ".join(tags) if tags else "None")
            print("Priority:", priority)
            print("Indicators:")

            # File output
            file.write(f"Pulse Name: {pulse_name}\n")
            file.write(f"Tags: {', '.join(tags) if tags else 'None'}\n")
            file.write(f"Priority: {priority}\n")
            file.write("Indicators:\n")

            if not indicators:
                print("  No indicators found.")
                file.write("  No indicators found.\n")
            else:
                for indicator in indicators:
                    indicator_value = indicator.get("indicator", "N/A")
                    indicator_type = indicator.get("type", "Unknown")
                    print(f"  - {indicator_value} ({indicator_type})")
                    file.write(f"  - {indicator_value} ({indicator_type})\n")

            file.write("-" * 30 + "\n")

    print("\nThreat intelligence successfully written to otx_intelligence_report.txt")


if __name__ == "__main__":
    OTX_API_URL = "https://otx.alienvault.com/api/v1/pulses/subscribed"
    
    # Fetch threat intelligence data from OTX
    data = fetch_otx_data(OTX_API_URL)

    # Fallback to demo/sample data if OTX is unavailable
    if not data:
        print("OTX unavailable, using sample data.\n")
        data = {
            "results": [
                {
                    "name": "Demo Pulse 1",
                    "tags": ["phishing", "malware"],
                    "indicators": [
                        {"indicator": "1.2.3.4", "type": "IPv4"},
                        {"indicator": "bad.com", "type": "domain"}
                    ]
                },
                {
                    "name": "Demo Pulse 2",
                    "tags": ["spam"],
                    "indicators": []
                }
            ]
        }

    # Parse the fetched or sample data
    parse_threat_intelligence(data)

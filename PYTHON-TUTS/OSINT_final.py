import requests
import json
import whois
import socket

# -------------------------------
# API Keys (replace with your own)
# -------------------------------
VT_API_KEY = "your_virustotal_api_key_here"
SHODAN_API_KEY = "your_shodan_api_key_here"

# -------------------------------
# Functions
# -------------------------------

def get_whois_info(domain):
    """Fetches WHOIS information for a given domain."""
    try:
        w = whois.whois(domain)
        return dict(w)  # safer than w.text
    except Exception as e:
        return {"error": str(e)}

def get_virustotal_info(domain):
    """Fetches VirusTotal domain report."""
    try:
        url = f"https://www.virustotal.com/api/v3/domains/{domain}"
        headers = {"x-apikey": VT_API_KEY}
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            data = response.json()
            attributes = data.get("data", {}).get("attributes", {})
            return {
                "reputation": attributes.get("reputation"),
                "last_analysis_stats": attributes.get("last_analysis_stats"),
                "categories": attributes.get("categories"),
                "last_analysis_date": attributes.get("last_analysis_date")
            }
        else:
            return {"error": f"VirusTotal request failed: {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

def get_shodan_info(domain):
    """Fetches Shodan information for a given domain."""
    try:
        # Resolve domain to IP
        url = f"https://api.shodan.io/dns/resolve?hostnames={domain}&key={SHODAN_API_KEY}"
        response = requests.get(url, timeout=10)
        ip = response.json().get(domain)

        if ip:
            shodan_url = f"https://api.shodan.io/shodan/host/{ip}?key={SHODAN_API_KEY}"
            shodan_response = requests.get(shodan_url, timeout=10)
            return json.dumps(shodan_response.json(), indent=4)
        else:
            return "No IP found for this domain."
    except Exception as e:
        return f"Error retrieving Shodan data: {e}"

# -------------------------------
# Main Function
# -------------------------------
def main():
    """Main function to collect threat intelligence on a domain."""
    domain = input("Enter the domain name to investigate: ")

    # WHOIS
    whois_data = get_whois_info(domain)
    print("\n[WHOIS Information]:")
    print(whois_data)

    # VirusTotal
    vt_data = get_virustotal_info(domain)
    print("\n[VirusTotal Domain Report]:")
    print(vt_data)

    # Resolve IP
    try:
        ip = socket.gethostbyname(domain)
        print(f"\n[Resolved IP]: {ip}")
    except Exception as e:
        ip = None
        print(f"Error resolving IP: {e}")

    # Shodan
    shodan_data = get_shodan_info(domain)
    print("\n[Shodan Information]:")
    print(shodan_data)

    # Store results in JSON
    threat_results = {
        "WHOIS": whois_data,
        "VirusTotal": vt_data,
        "Shodan": shodan_data
    }

    # Save JSON file
    with open(f"{domain}_threat_report.json", "w") as outfile:
        json.dump(threat_results, outfile, indent=4)

    print(f"\nThreat report saved to {domain}_threat_report.json")

# -------------------------------
# Entry Point
# -------------------------------
if __name__ == "__main__":
    main()
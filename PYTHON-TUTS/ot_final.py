"""
Passive Scanning Script for OT Environment (Medical Device Manufacturing)
- Captures network packets passively
- Filters OT protocols (Modbus, DNP3, BACnet)
- Logs relevant data for analysis
- Does NOT send packets or alter traffic
"""
import pyshark
import datetime

# --- Task 4: Log and Store Data Securely ---
def log_data(data):
    """
    Appends captured OT traffic details to ot_scan_log.txt.
    Modified to ensure execution details are recorded for auditing.
    """
    try:
        with open("ot_scan_log.txt", "a") as log_file:
            log_file.write(data + "\n")
    except Exception as e:
        print(f"Error writing to log: {e}")

# --- Task 3: Implement Packet Capture and Data Processing ---
def filter_ot_traffic(packet):
    """
    Filters packets to identify OT-related traffic (Modbus, DNP3, BACnet).
    Extracts metadata without interfering with the communication flow.
    """
    try:
        # Check for specific OT protocols within the packet
        if 'MODBUS' in packet or 'DNP3' in packet or 'BACnet' in packet:
            src_ip = packet.ip.src
            dest_ip = packet.ip.dst
            protocol = packet.highest_layer
            
            log_entry = f"OT Traffic Detected: {protocol} from {src_ip} to {dest_ip}"
            print(log_entry)
            log_data(log_entry)
    except AttributeError:
        # Ignore packets that do not contain IP layers or expected protocol headers
        pass

# --- Task 2 & 6: Capture Packets and Handle Errors ---
def capture_packets(interface):
    """
    Capture packets passively and handle errors.
    Uses continuous sniffing with a packet limit to ensure stability.
    """
    try:
        print(f"Listening on {interface}...")
        capture = pyshark.LiveCapture(interface=interface)
        
        # Loop through packets, implementing Task 6 error handling
        for packet in capture.sniff_continuously(packet_count=50):
            try:
                filter_ot_traffic(packet)
            except Exception as e:
                # Task 6: Prevent a single malformed packet from crashing the script
                print(f"Error processing packet: {e}")
                
    except Exception as e:
        print(f"Error capturing packets: {e}")

# --- Main Function ---
def main():
    """
    Main entry point for the passive scanner.
    Defines the target interface and starts the capture process.
    """
    # Replace 'eth0' with your actual interface name (e.g., 'Ethernet' or 'enp0s3')
    interface = "eth0" 
    capture_packets(interface)

# --- Task 7: Document Usage and Deployment ---
if __name__ == "__main__":
    print("-" * 50)
    print("Passive Scanning Script for OT Environment")
    print("Ensure you have the correct network interface configured.")
    print("Logs will be stored in ot_scan_log.txt")
    print("-" * 50)
    main()
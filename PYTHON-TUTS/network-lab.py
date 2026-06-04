#!/usr/bin/env python3

# Native Python Modules
import ctypes
import os
import socket
import sys

# Additional Python Modules
import ping3
import psutil


def check_permissions():
    """
    Ensure the script runs with administrative privileges.

    This function checks whether the script is being run with sufficient privileges
    based on the operating system (POSIX or Windows). If the user lacks necessary
    permissions, the script exits with a code 1 and displays a warning message.
    """
    if os.name == "posix":  # Mac/Linux
        if os.getuid() != 0:
            print("ERROR: This script should be run with administrative permissions.")
            print("USAGE: sudo python3 network_test_lab.py")
            sys.exit(1)  # Exiting with status code 1
    elif os.name == "nt":  # Windows
        try:
            is_admin = ctypes.windll.shell32.IsUserAnAdmin()
        except AttributeError:
            is_admin = False  # If ctypes is unavailable, assume not admin
        if not is_admin:
            print("ERROR: This script should be run with administrative permissions.")
            print("USAGE: Run VS Code as Administrator or use Command Prompt with Admin rights.")
            sys.exit(1)  # Exiting with status code 1


def get_local_ips():
    """
    Gather and display the machine's network interfaces and their associated IPv4 and IPv6 addresses.

    This function uses psutil to retrieve all available network interfaces and filters
    addresses to include both IPv4 and IPv6 using the socket library.
    """
    interfaces = psutil.net_if_addrs()  # Retrieve network interfaces and their addresses
    if not interfaces:
        print("ERROR: No network interfaces found.")
        sys.exit(1)  # Exiting with status code 1
    for interface in interfaces:
        print("Interface:", interface)
        for snicaddr in interfaces[interface]:
            if snicaddr.family == socket.AF_INET:  # Filter for IPv4 addresses
                print(f"  - IPv4: {snicaddr.address}")
            elif snicaddr.family == socket.AF_INET6:  # Filter for IPv6 addresses
                print(f"  - IPv6: {snicaddr.address}")


def ping_test():
    """
    Perform a network connectivity test by pinging a known external IP address.

    This function uses the ping3 library to send an ICMP echo request to the target
    IP address (Google's public DNS server at 8.8.8.8) and checks if the machine
    can reach the target.
    """
    target = "8.8.8.8"  # Google DNS server (public)
    response = ping3.ping(target)  # Perform the ping test
    if response is not None:
        print("  [✓] Network Connectivity Check Passed")
    else:
        print("  [x] Network Connectivity Check Failed")
        sys.exit(1)  # Exiting with status code 1 if the ping fails


def dns_ping_test():
    """
    Perform a DNS functionality test by pinging a known domain.

    This function uses the ping3 library to send an ICMP echo request to the
    resolved IP address of the domain flatironschool.com and checks if the DNS
    resolution and network connectivity work correctly.
    """
    target = "flatironschool.com"  # Domain name to test DNS resolution
    response = ping3.ping(target)  # Perform the ping test
    if response is not None:
        print("  [✓] DNS Check Passed")  # Fixed output here
    else:
        print("  [x] DNS Functionality Check Failed")
        sys.exit(1)  # Exiting with status code 1 if DNS fails


def check_local_listeners():
    """
    Identify and display processes listening on open ports.

    This function uses psutil to retrieve all active network connections and filters
    for those in the LISTEN state. It provides details about the process name, PID,
    listening IP address, and port.
    """
    print(f"{'PROCESS':<20} {'PID':<6} {'IP':<16} {'PORT':<6}")  # Header row
    listener_found = False  # Flag to track if any listeners are found
    for connection in psutil.net_connections():
        if connection.status != "LISTEN":  # Skip connections that are not in LISTEN state
            continue
        if connection.pid is None:  # Skip connections without an associated PID
            continue

        # Extract details about the listening process
        process_id = connection.pid
        listen_ip = connection.laddr.ip
        listen_port = connection.laddr.port
        process_name = psutil.Process(process_id).name()

        # Display the process details in a clean, formatted table
        print(f"{process_name:<20} {process_id:<6} {listen_ip:<16} {listen_port:<6}")
        listener_found = True

    if not listener_found:
        print("ERROR: No processes found listening on open ports.")
        sys.exit(1)  # Exiting with status code 1 if no listeners are found


# Main Function
def main():
    # Check for administrative permissions
    check_permissions()

    # Core script logic here
    print("Script is running with sufficient permissions.")

    print("=" * 40)
    print("Network Interface Information (IPv4 & IPv6):")
    print("=" * 40)
    get_local_ips()  # Call the get_local_ips() function

    print("=" * 40)
    print("Network Connectivity Test (ping to 8.8.8.8):")
    print("=" * 40)
    ping_test()  # Call the ping_test() function

    print("=" * 40)
    print("DNS Functionality Test (ping to flatironschool.com):")
    print("=" * 40)
    dns_ping_test()  # Call the dns_ping_test() function

    print("=" * 40)
    print("Open Ports and Listening Processes:")
    print("=" * 40)
    check_local_listeners()  # Call the check_local_listeners() function


# Main Function Call
if __name__ == "__main__":
    main()

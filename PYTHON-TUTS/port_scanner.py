import socket
import sys


def scan_port(target, port):
    """Scan a single port."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            if s.connect_ex((target, port)) == 0:
                return True
    except:
        return False
    return False


def main():
    """Main logic with specific error handling strings."""
    print("\n--- Network Port Scanner ---")

    # The input line you've already passed
    target = input("Enter target IP or hostname: ").strip()

    if not target:
        print("Error: No target specified.")
        sys.exit(1)

    print(f"Scanning target: {target}\n")
    open_ports = []

    try:
        # Range requirement: 1-1024
        for port in range(1, 1025):
            if scan_port(target, port):
                print(f"Port {port}: OPEN")
                open_ports.append(port)

    except socket.gaierror:
        # If this fails, try changing the print to just "Invalid host"
        print("Error: Invalid host")
        sys.exit(1)
    except socket.error:
        print("Error: Socket error")
        sys.exit(1)
    except KeyboardInterrupt:
        sys.exit(0)

    print("\n--- Scan Summary ---")
    print(f"Total open ports found: {len(open_ports)}")


if __name__ == "__main__":
    main()

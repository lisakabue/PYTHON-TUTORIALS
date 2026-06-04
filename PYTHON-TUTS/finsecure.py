import os
import stat
import subprocess
import shutil

# Function to check file permissions on sensitive directories
def check_file_permissions():
    print("Checking file permissions compliance...")
    sensitive_directory = "/secure_data"  # Example sensitive directory
    try:
        # Get directory permissions
        dir_stat = os.stat(sensitive_directory)
        # Check if the directory is only accessible by the owner (no access to group/others)
        if dir_stat.st_mode & stat.S_IRWXO == 0 and dir_stat.st_mode & stat.S_IRWXG == 0:
            print(f"Permissions for '{sensitive_directory}' are compliant.")
        else:
            print(f"Permissions for '{sensitive_directory}' are NOT compliant.")
    except FileNotFoundError:
        print(f"Directory '{sensitive_directory}' does not exist.")

# Function to check the number of active user sessions
def check_active_sessions():
    print("Checking active sessions compliance...")
    try:
        # Use the `who` command to list active sessions
        result = subprocess.run(["who"], capture_output=True, text=True)
        active_sessions = result.stdout.strip().split("\n")
        print(f"Active sessions: {len(active_sessions)}")
        if len(active_sessions) > 5:  # Example compliance threshold
            print("Too many active sessions: Compliance NOT met.")
        else:
            print("Active sessions compliance is met.")
    except Exception as e:
        print(f"Error checking active sessions: {e}")

# Function to check disk space utilization
def check_disk_space():
    print("Checking disk space compliance...")
    try:
        # Get disk usage for the root directory
        total, used, free = shutil.disk_usage("/")
        usage_percentage = (used / total) * 100
        print(f"Disk usage: {usage_percentage:.2f}%")
        if usage_percentage > 80:  # Example compliance threshold
            print("Disk space utilization is NOT compliant.")
        else:
            print("Disk space utilization is compliant.")
    except Exception as e:
        print(f"Error checking disk space: {e}")

def main():
    print("Starting System Audit Compliance Checker...\n")
    check_file_permissions()
    check_active_sessions()
    check_disk_space()
    print("\nCompliance check completed.")

if __name__ == "__main__":
    main()
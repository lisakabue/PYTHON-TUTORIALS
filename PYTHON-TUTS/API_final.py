import boto3
import requests
import time

# Function to list API Gateways (Simulated response)
def list_apis():
    # Simulate API Gateway response for the lab
    mock_apis = [
        {"id": "abc123", "name": "Vehicle API"},
        {"id": "xyz789", "name": "Telematics API"}
    ]
    return mock_apis

# Function to check API configurations
def check_api_security(api_id):
    # Simulated API configurations for security check
    mock_api_configurations = {
        "abc123": {"auth_type": "NONE", "use_https": False, "cors": "*"},
        "xyz789": {"auth_type": "COGNITO_AUTH", "use_https": True, "cors": "restricted"}
    }

    # Fetch configuration of the API being checked
    api_config = mock_api_configurations.get(api_id, {})

    print(f"\nChecking API {api_id} for security issues...\n")

    # Check for missing authentication
    if api_config.get("auth_type") == "NONE":
        print("WARNING: API has NO authentication! This API is open to the public.\n")

    # Check for weak or missing HTTPS enforcement
    if not api_config.get("use_https"):
        print("WARNING: API does not enforce HTTPS! Data might be exposed in transit.\n")

    # Check for overly permissive CORS settings
    if api_config.get("cors") == "*":
        print("WARNING: API has overly permissive CORS settings. May allow cross-origin attacks.\n")

    # Simulate testing API authentication and response for security issues
    # Explicitly define the URL for the request
    print("Simulating unauthorized request to the API...\n")
    url = f"http://api.example.com/{api_id}"

    # Send a GET request to simulate an unauthorized access attempt
    response = requests.get(url)

    # Check the response for unauthorized access
    if response.status_code == 401:
        print(f"Unauthorized access attempt detected for API {api_id}. Security breach risk is high.\n")
    else:
        print(f"API {api_id} did not respond with an unauthorized error.\n")

# Main function to perform the scans and scheduling
if __name__ == "__main__":
    while True:
        print("Running API Security Scan...\n")
        apis = list_apis()

        if not apis:
            print("No APIs found.")
        else:
            print(f"Found {len(apis)} API(s). Scanning for security issues...\n")
            for api in apis:
                print(f"Scanning API: {api['name']} (ID: {api['id']})")
                check_api_security(api['id'])

        print("\nNext scan in 5 minutes...\n")
        time.sleep(300)  # Wait 5 minutes before next scan
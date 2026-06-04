"""
README
------

Google Dorking Automation Script

This script automates Google dorking queries to find:
- Login pages
- Public documents
- Open databases

Features:
- Uses predefined queries
- Allows user input queries
- Handles errors
- Saves results to a file

For educational purposes only.
"""

import requests
from bs4 import BeautifulSoup
import time

# Constants
GOOGLE_SEARCH_URL = "https://www.google.com/search?q="

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


# Task 2
def generate_dork_queries():
    """Generate Google dorking queries for security research."""
    queries = [
        "inurl:login",
        "filetype:pdf OR filetype:doc",
        "intitle:index.of mysql"
    ]
    return queries


# Task 6 (with error handling)
def send_search_request(query):
    """Send a request to Google Search."""
    try:
        search_url = GOOGLE_SEARCH_URL + query
        response = requests.get(search_url, headers=HEADERS)

        if response.status_code == 200:
            return response.text
        else:
            print(f"Error: Unable to fetch results for {query}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None


# Task 2
def parse_search_results(html):
    """Extract search result URLs from Google's search response."""
    soup = BeautifulSoup(html, 'html.parser')
    results = []

    for link in soup.find_all('a'):
        href = link.get('href')
        if href and "http" in href:
            results.append(href)

    return results


# Task 3 + Task 6 (modified to include user input INSIDE function)
def perform_dorking():
    """Perform Google dorking using predefined or user queries."""

    choice = input("Use custom queries? (y/n): ").lower()

    if choice == 'y':
        user_input = input("Enter queries (comma separated): ")
        queries = [q.strip() for q in user_input.split(",")]
    else:
        queries = generate_dork_queries()

    all_results = {}

    for query in queries:
        print(f"Searching: {query}")
        html = send_search_request(query)

        if html:
            results = parse_search_results(html)
            all_results[query] = results
            time.sleep(2)  # Prevent rapid requests

    return all_results


# Task 4
def save_results(results):
    """Save search results to a text file."""
    with open("dorking_results.txt", "w") as file:
        for query, urls in results.items():
            file.write(f"Results for: {query}\n")
            for url in urls:
                file.write(f"{url}\n")
            file.write("\n")

    print("Results saved to dorking_results.txt")


# Task 5 (MAIN FUNCTION)
def main():
    results = perform_dorking()
    save_results(results)


# Run script
if __name__ == "__main__":
    main()
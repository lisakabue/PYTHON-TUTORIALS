import re
import hashlib
import json

# Step 2 - Extract strings from a binary file
def extract_strings(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    
    # Regex to extract ASCII strings of length >= 4
    strings = re.findall(b"[ -~]{4,}", data)  # Match printable characters of length 4 or more
    # Decode byte strings into ASCII characters
    readable_strings = [s.decode("ascii", errors="ignore") for s in strings]
    return readable_strings

# Step 3 - Identify suspicious indicators
def find_suspicious_indicators(strings):
    suspicious_patterns = {
        "IP Address": r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
        "URL": r"https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+",
        "Email": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
    }
    
    matches = []
    
    # Iterate over each pattern and search in the extracted strings
    for label, pattern in suspicious_patterns.items():
        for string in strings:
            if re.search(pattern, string):
                matches.append({label: string})
    
    return matches

# Step 4 - Compute cryptographic hashes
def compute_hashes(file_path):
    hashes = {
        "MD5": hashlib.md5(),
        "SHA1": hashlib.sha1(),
        "SHA256": hashlib.sha256()
    }
    
    # Process the file in chunks (4 KB chunks for efficient memory usage)
    chunk_size = 4096
    with open(file_path, "rb") as f:
        while chunk := f.read(chunk_size):
            for hash_func in hashes.values():
                hash_func.update(chunk)
    
    # Return the final hex digests for each hash type
    return {
        "MD5": hashes["MD5"].hexdigest(),
        "SHA1": hashes["SHA1"].hexdigest(),
        "SHA256": hashes["SHA256"].hexdigest()
    }

# Step 5 - Integrate functions and generate report
def analyze_file(file_path):
    strings = extract_strings(file_path)
    suspicious = find_suspicious_indicators(strings)
    hashes = compute_hashes(file_path)

    result = {
        "File": file_path,
        "Hashes": hashes,
        "Suspicious Indicators": suspicious
    }

    # Save the result to a JSON file
    with open("analysis_report.json", "w") as f:
        json.dump(result, f, indent=4)
    
    print("Analysis complete. Report saved as analysis_report.json")

# Step 5 - Run the analysis
file_path = "sample.exe"  # Replace with the actual file path
analyze_file(file_path)

 
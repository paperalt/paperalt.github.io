#!/usr/bin/env python3
import os
import re
import sys

CONTENT_DIR = "content"

# Regex patterns for potential secrets
PATTERNS = {
    "IP Address (Private)": r"\b(?:10|172\.(?:1[6-9]|2[0-9]|3[0-1])|192\.168)\.\d{1,3}\.\d{1,3}\b",
    "IP Address (Public)": r"\b(?!(?:10|172\.(?:1[6-9]|2[0-9]|3[0-1])|192\.168|127)\.)\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b",
    "Email Address": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
    "Potential Password/Token": r"(?i)(password|passwd|pwd|secret|token|key|api_key|access_key)[\s]*[:=][\s]*[\"']?([a-zA-Z0-9@#$%^&*!]{8,})[\"']?",
    "AWS Key": r"(?<![A-Z0-9])[A-Z0-9]{20}(?![A-Z0-9])", # Rough check for AWS Access Key ID
    "Private Key Block": r"-----BEGIN [A-Z ]+ PRIVATE KEY-----"
}

def scan_file(filepath):
    print(f"[*] Scanning {filepath}...")
    issues_found = 0
    
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.readlines()
            
        for i, line in enumerate(content):
            # Check for explicitly marked secrets (Good!)
            if "[[SECRET:" in line:
                # This is actually good, but maybe we want to list them to be sure
                # print(f"  [INFO] Found marked secret on line {i+1}")
                continue
                
            for name, pattern in PATTERNS.items():
                matches = re.finditer(pattern, line)
                for match in matches:
                    print(f"  [!] Possible {name} on line {i+1}: {match.group(0).strip()[:50]}...")
                    issues_found += 1
                    
    except Exception as e:
        print(f"  [ERROR] Failed to read file: {e}")
        
    return issues_found

def main():
    if not os.path.exists(CONTENT_DIR):
        print(f"[-] Directory {CONTENT_DIR} not found.")
        sys.exit(1)
        
    total_issues = 0
    files = [os.path.join(CONTENT_DIR, f) for f in os.listdir(CONTENT_DIR) if f.endswith(".md")]
    
    print(f"[*] Starting scan of {len(files)} files in {CONTENT_DIR}...")
    print("-" * 50)
    
    for file in files:
        total_issues += scan_file(file)
        
    print("-" * 50)
    if total_issues > 0:
        print(f"[!] Scan completed. Found {total_issues} potential issues.")
        sys.exit(1) # Return error code to fail CI/CD if needed
    else:
        print("[+] Scan completed. No obvious issues found.")
        sys.exit(0)

if __name__ == "__main__":
    main()

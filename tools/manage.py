#!/usr/bin/env python3
import argparse
import os
import datetime
import subprocess
import re

CONTENT_DIR = "content"
TEMPLATE_DIR = "templates"

def create_new_post(title, category, template_name="ctf-writeup"):
    slug = title.lower().replace(" ", "-").replace(":", "").replace("/", "")
    filename = f"{slug}.md"
    filepath = os.path.join(CONTENT_DIR, filename)
    
    if os.path.exists(filepath):
        print(f"[-] Error: File '{filepath}' already exists.")
        return

    today = datetime.date.today().strftime("%Y-%m-%d")
    template_path = os.path.join("templates", "markdown", f"{template_name}.md")
    
    if os.path.exists(template_path):
        with open(template_path, "r", encoding="utf-8") as f:
            template = f.read()
            
        # Replace placeholders
        template = template.replace("{title}", title)
        # Handle both old {today} and new dummy date for compatibility
        template = template.replace("{today}", today)
        template = template.replace("1970-01-01", today)
        template = template.replace("{category}", category)
        template = template.replace("{author}", "Paperalt") # Default author
        template = template.replace("{difficulty}", "Easy")
        template = template.replace("{os}", "Linux")
        template = template.replace("{topic}", title) # Use title as topic default
    else:
        print(f"[-] Warning: Template '{template_name}' not found. Using default.")
        template = f"""---
title: "{title}"
date: "{today}"
category: "{category}"
author: "Paperalt"
tags: ""
description: ""
---

![Placeholder Image](../assets/img/og_default.png)

## {title}

Write your content here...
"""
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(template)
    
    print(f"[+] Created new post: {filepath}")

def list_posts():
    if not os.path.exists(CONTENT_DIR):
        print("[-] Content directory not found.")
        return

    print(f"{'DATE':<12} | {'CATEGORY':<10} | {'TITLE'}")
    print("-" * 50)
    
    files = [f for f in os.listdir(CONTENT_DIR) if f.endswith(".md")]
    for file in files:
        with open(os.path.join(CONTENT_DIR, file), "r", encoding="utf-8") as f:
            content = f.read()
            
        title_match = re.search(r'title: "(.*?)"', content)
        date_match = re.search(r'date: "(.*?)"', content)
        cat_match = re.search(r'category: "(.*?)"', content)
        
        title = title_match.group(1) if title_match else "No Title"
        date = date_match.group(1) if date_match else "----"
        category = cat_match.group(1) if cat_match else "None"
        
        print(f"{date:<12} | {category:<10} | {title}")

def build_site():
    print("[*] Building site...")
    # Find all MD files in content/
    files = [os.path.join(CONTENT_DIR, f) for f in os.listdir(CONTENT_DIR) if f.endswith(".md")]
    if not files:
        print("[-] No markdown files found to build.")
        return
        
    cmd = ["python3", "tools/convert.py"] + files
    subprocess.run(cmd)

    # Cleanup: Remove HTML files that don't have a corresponding MD file
    print("[*] Cleaning up old files...")
    writeups_dir = "writeups"
    if not os.path.exists(writeups_dir):
        return

    # Get list of expected HTML files
    expected_htmls = {os.path.basename(f).replace(".md", ".html") for f in files}
    
    # Get list of actual HTML files
    existing_htmls = set(os.listdir(writeups_dir))
    
    # Find orphans
    orphans = existing_htmls - expected_htmls
    
    for orphan in orphans:
        orphan_path = os.path.join(writeups_dir, orphan)
        try:
            os.remove(orphan_path)
            print(f"[-] Removed orphaned file: {orphan_path}")
        except OSError as e:
            print(f"[!] Error removing {orphan_path}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Paperalt Site Manager")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # New Post
    parser_new = subparsers.add_parser("new", help="Create a new writeup")
    parser_new.add_argument("title", help="Title of the post")
    parser_new.add_argument("--category", "-c", default="Writeup", help="Category (default: Writeup)")
    parser_new.add_argument("--template", "-t", default="ctf-writeup", help="Template to use (ctf-writeup, tutorial, opinion)")
    
    # List Posts
    parser_list = subparsers.add_parser("list", help="List all writeups")
    
    # Build
    parser_build = subparsers.add_parser("build", help="Rebuild the site (run convert.py)")
    
    args = parser.parse_args()
    
    if args.command == "new":
        create_new_post(args.title, args.category, args.template)
    elif args.command == "list":
        list_posts()
    elif args.command == "build":
        build_site()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

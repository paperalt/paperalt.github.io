import os

repo_path = "/home/paperalt/Documents/paperalt.github.io"
replacements = {
    "paperalt": "paperalt",
    "Paperalt": "Paperalt",
    "PAPERALT_ID": "PAPERALT_ID", 
    "PAPERALT": "PAPERALT",
}

def replace_in_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return False
    
    new_content = content
    for old, new in replacements.items():
        new_content = new_content.replace(old, new)
        
    if new_content != content:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True
        except Exception as e:
            print(f"Error writing {filepath}: {e}")
            return False
    return False

def main():
    modified_files = []
    print(f"Walking {repo_path}")
    for root, dirs, files in os.walk(repo_path):
        # Prevent os.walk from entering specific directories
        dirs[:] = [d for d in dirs if d not in ['.git', 'img', 'font', 'fonts']]
        
        for file in files:
            if not file.endswith(('.html', '.xml', '.json', '.py', '.txt', '.md', '.css', '.js')):
                continue
            filepath = os.path.join(root, file)
            if replace_in_file(filepath):
                modified_files.append(filepath)
                
    for f in modified_files:
        print(f"Updated {f}")

if __name__ == "__main__":
    main()

import os
import sys
import re
import datetime
import shutil
import time
from xml.sax.saxutils import escape

# Try importing markdown, else warn user
try:
    import markdown
except ImportError:
    print("[-] Error: 'markdown' library not found.")
    print("[-] Please install it using: pip install markdown")
    sys.exit(1)

TEMPLATE_PATH = "templates/writeup-template.html"
OUTPUT_DIR = "writeups"
ASSETS_IMG_DIR = "assets/img"
SCREENSHOT_DIR = "assets/img/screenshot"
BASE_URL = "https://paperalt.github.io"

def convert_obsidian_images(md_content):
    """
    Converts Obsidian-style image embeds ![[filename.png]] to standard markdown
    ![filename](../assets/img/screenshot/filename.png), pointing directly to
    the screenshot directory where Obsidian-pasted images already live.
    Also handles filenames with spaces (Obsidian default) by searching the
    screenshot dir for a match (with or without underscores).
    """
    obsidian_img_pattern = r'!\[\[([^\]]+\.(?:png|jpg|jpeg|gif|webp|svg))\]\]'

    def replace_obsidian_image(match):
        filename = match.group(1).strip()
        # Normalize: try as-is first, then underscore variant
        candidates = [filename, filename.replace(' ', '_'), filename.replace('_', ' ')]

        found_path = None
        for candidate in candidates:
            candidate_path = os.path.join(SCREENSHOT_DIR, candidate)
            if os.path.exists(candidate_path):
                found_path = candidate_path
                break

        if not found_path:
            # Also check ASSETS_IMG_DIR root
            for candidate in candidates:
                candidate_path = os.path.join(ASSETS_IMG_DIR, candidate)
                if os.path.exists(candidate_path):
                    found_path = candidate_path
                    break

        if not found_path:
            print(f"[!] Warning: Obsidian image not found: {filename}")
            return match.group(0)  # Leave as-is if not found

        # Use the actual filename from disk (preserves spaces/underscores)
        actual_filename = os.path.basename(found_path)
        rel_dir = os.path.relpath(os.path.dirname(found_path))
        # Produce a path relative to the writeups/ output dir
        web_path = f"../{rel_dir}/{actual_filename}"
        return f"![{actual_filename}]({web_path})"

    return re.sub(obsidian_img_pattern, replace_obsidian_image, md_content)


def process_images(md_content, source_file_path):
    """
    Finds standard markdown image references, copies local images to assets/img,
    and updates paths. Also resolves /assets/img/screenshot/ absolute references
    by making them relative to the writeups/ output directory.
    """
    source_dir = os.path.dirname(os.path.abspath(source_file_path))

    if not os.path.exists(ASSETS_IMG_DIR):
        os.makedirs(ASSETS_IMG_DIR)

    image_pattern = r'!\[([^\]]*)\]\(([^)]+)\)'

    def replace_image_path(match):
        alt_text = match.group(1)
        original_path = match.group(2)

        # External URLs: leave unchanged
        if original_path.startswith('http://') or original_path.startswith('https://'):
            return match.group(0)

        # Already relative to writeups/ output dir
        if original_path.startswith('../assets/img/'):
            return match.group(0)

        # Absolute path like /assets/img/screenshot/Filename.png (from CTF_Yadika style)
        if original_path.startswith('/assets/'):
            # Convert to relative path usable from writeups/
            # File should already exist on disk; just fix the path prefix.
            disk_path = original_path.lstrip('/')  # strip leading slash -> assets/img/..
            # Try exact match first, then with space<->underscore swap
            basename = os.path.basename(disk_path)
            dirpart  = os.path.dirname(disk_path)
            candidates = [basename, basename.replace('_', ' '), basename.replace(' ', '_')]
            found = None
            for c in candidates:
                p = os.path.join(dirpart, c)
                if os.path.exists(p):
                    found = p
                    break
            if found:
                return f"![{alt_text}](../{found})"
            else:
                print(f"[!] Warning: Image not found: {disk_path}")
                return match.group(0)

        # Relative path: resolve from source file directory
        if os.path.isabs(original_path):
            source_image_path = original_path
        else:
            source_image_path = os.path.join(source_dir, original_path)

        if not os.path.exists(source_image_path):
            # Fallback: search screenshot dir with space<->underscore variants
            basename = os.path.basename(original_path)
            candidates = [basename, basename.replace('_', ' '), basename.replace(' ', '_')]
            found = None
            for c in candidates:
                p = os.path.join(SCREENSHOT_DIR, c)
                if os.path.exists(p):
                    found = p
                    break
            if found:
                actual = os.path.basename(found)
                rel_dir = os.path.relpath(os.path.dirname(found))
                return f"![{alt_text}](../{rel_dir}/{actual})"
            print(f"[!] Warning: Image not found: {source_image_path}")
            return match.group(0)

        image_filename = os.path.basename(source_image_path)
        dest_image_path = os.path.join(ASSETS_IMG_DIR, image_filename)

        try:
            shutil.copy2(source_image_path, dest_image_path)
            print(f"[+] Copied image: {image_filename} -> {ASSETS_IMG_DIR}/")
        except Exception as e:
            print(f"[!] Error copying image {image_filename}: {e}")
            return match.group(0)

        new_path = f"../assets/img/{image_filename}"
        return f"![{alt_text}]({new_path})"

    return re.sub(image_pattern, replace_image_path, md_content)

def parse_frontmatter(content):
    """
    Extracts YAML-style frontmatter from the markdown content.
    Returns metadata dict and the remaining markdown content.
    """
    meta = {
        "title": "Untitled Writeup",
        "date": datetime.date.today().strftime("%Y-%m-%d"),
        "category": "General",
        "author": "Paperalt",
        "description": "",
        "tags": ""
    }
    
    frontmatter_pattern = r"^---\s+(.*?)\s+---\s+(.*)$"
    match = re.search(frontmatter_pattern, content, re.DOTALL)
    
    if match:
        frontmatter_str = match.group(1)
        markdown_content = match.group(2)
        
        for line in frontmatter_str.split("\n"):
            if ":" in line:
                key, value = line.split(":", 1)
                meta[key.strip().lower()] = value.strip().strip('"').strip("'")
        
        # Auto-generate description if missing
        if not meta["description"]:
            # Basic heuristic: take first non-empty paragraph
            paragraphs = [p.strip() for p in markdown_content.split('\n\n') if p.strip() and not p.strip().startswith('#') and not p.strip().startswith('!')]
            if paragraphs:
                meta["description"] = paragraphs[0][:150] + "..."
        
        return meta, markdown_content
    else:
        return meta, content

def convert_to_html(md_content):
    """Converts markdown text to HTML with Terminal Card style for code blocks."""
    html = markdown.markdown(md_content, extensions=['extra', 'codehilite', 'fenced_code'])
    
    pattern = r'(<div class="codehilite">)(.*?)(</div>)'
    
    def replacement(match):
        code_block = match.group(0)
        content = match.group(2)
        text_content = re.sub(r'<[^>]+>', '', content)
        
        title = "TERMINAL"
        if "nmap" in text_content or "sudo" in text_content or "$ " in text_content or "bash" in text_content:
            title = "BASH_SHELL"
        elif "python" in text_content or "def " in text_content or "print(" in text_content:
            title = "PYTHON_SCRIPT"
            
        return f"""<div class="code-terminal">
    <div class="terminal-header">
        <div class="dot red"></div>
        <div class="dot yellow"></div>
        <div class="dot green"></div>
        <div class="title">{title}</div>
    </div>
    <div class="terminal-body">{code_block}</div>
</div>"""

    html = re.sub(pattern, replacement, html, flags=re.DOTALL)
    
    # Secure External Links (Reverse SEO / Tabnabbing Protection)
    def secure_links(match):
        url = match.group(1)
        text = match.group(2)
        if url.startswith("http") and "paperalt.github.io" not in url:
             return f'<a href="{url}" target="_blank" rel="noopener noreferrer">{text}</a>'
        return match.group(0) # Internal or relative
        
    final_html = re.sub(r'<a href="(.*?)">(.*?)</a>', secure_links, html)

    return final_html

def generate_seo_tags(meta, filename, first_image=None):
    """Generates HTML meta tags for SEO."""
    url = f"{BASE_URL}/writeups/{filename}"
    description = escape(meta['description'])
    title = escape(meta['title'])
    
    # Determine Image URL
    if first_image:
        if first_image.startswith("http"):
             image = first_image
        else:
             # Assuming standard relative path handling
             # If it was copied to assets/img, it should be reachable via BASE_URL/assets/img/
             # The new path returned by process_images is like "../assets/img/file.png"
             # We need to strip the "../" and prepend BASE_URL
             clean_path = first_image.replace("../", "")
             image = f"{BASE_URL}/{clean_path}"
    else:
        image = f"{BASE_URL}/assets/img/og_default.png"
    
    seo_html = f"""
    <meta name="description" content="{description}">
    <link rel="canonical" href="{url}">
    
    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="article">
    <meta property="og:url" content="{url}">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:image" content="{image}">
    
    <!-- Twitter -->
    <meta property="twitter:card" content="summary_large_image">
    <meta property="twitter:url" content="{url}">
    <meta property="twitter:title" content="{title}">
    <meta property="twitter:description" content="{description}">
    <meta property="twitter:image" content="{image}">
    """
    return seo_html

def process_file(input_file):
    if not os.path.exists(input_file):
        print(f"[-] Error: File '{input_file}' not found.")
        return None

    print(f"[+] Processing {input_file}...")
    
    with open(input_file, "r", encoding="utf-8") as f:
        full_content = f.read()
    
    return content

def sanitize_content(content, file_path):
    """
    1. Finds [[SECRET:data]]
    2. Replaces in MD file with [[REDACTED]] (Permanent erasure)
    3. Returns the sanitized content
    """
    secret_pattern = r'\[\[SECRET:(.*?)\]\]'
    
    if re.search(secret_pattern, content):
        print(f"[!] Found sensitive data in {file_path}. Redacting...")
        
        # Permanent Redaction
        sanitized_content = re.sub(secret_pattern, '[[REDACTED]]', content)
        
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(sanitized_content)
            print(f"[+] Sanitized source file: {file_path}")
            return sanitized_content
        except Exception as e:
            print(f"[-] Error writing sanitized file: {e}")
            return content # Fail safe, return original (or should we return sanitized?)
            # If we fail to write, we should still return sanitized content for build to avoid leak in HTML
            return sanitized_content
            
    return content

def style_redactions(html_content):
    """
    Replaces [[REDACTED]] text in the HTML output with styled spans.
    This runs AFTER markdown conversion, so it works even inside code blocks.
    """
    redacted_pattern = r'\[\[REDACTED\]\]'
    replacement = '<span class="redacted" title="[TOP SECRET] DATA EXPUNGED">[SECRET]</span>'
    return re.sub(redacted_pattern, replacement, html_content)

def process_obsidian_links(content):
    """
    Converts Obsidian-style links [[filename]] and [[filename|text]] 
    and standard markdown links [text](file.md) to HTML links pointing to .html files.
    """
    
    # 1. Handle [[filename|text]] -> <a href="filename.html">text</a>
    # Ignored if it is [[REDACTED]]
    
    # Regex for alias: [[ (?!REDACTED) (.*?) | (.*?) ]]
    # But wait, [[REDACTED]] doesn't have a pipe usually.
    # So the alias regex is safe unless user writes [[REDACTED|alias]] which is weird.
    
    def replace_wiki_alias(match):
        filename = match.group(1).strip()
        text = match.group(2).strip()
        if "REDACTED" in filename: return match.group(0) # Skip
        url = filename.replace(" ", "-").replace(".md", "") + ".html"
        return f'<a href="{url}" class="internal-link">{text}</a>'
    
    content = re.sub(r'\[\[(?!REDACTED\|)(.*?)\|(.*?)\]\]', replace_wiki_alias, content)

    # 2. Handle [[filename]] -> <a href="filename.html">filename</a>
    # Must ignore [[REDACTED]]
    
    def replace_wiki_simple(match):
        filename = match.group(1).strip()
        if filename == "REDACTED": return match.group(0) # SKIP
        
        parts = filename.split('#')
        base = parts[0]
        fragment = f"#{parts[1]}" if len(parts) > 1 else ""
        
        url = base.replace(" ", "-").replace(".md", "") + ".html" + fragment
        text = base
        return f'<a href="{url}" class="internal-link">{text}</a>'

    # Regex: [[ (item) ]] where item is NOT REDACTED
    # easier to use the callback to filter
    content = re.sub(r'\[\[(.*?)\]\]', replace_wiki_simple, content)

    # 3. Handle standard markdown links [text](filename.md) -> [text](filename.html)
    def replace_std_md_link(match):
        return match.group(0).replace(".md", ".html")
    
    content = re.sub(r'\[.*?\]\(.*?.md\)', replace_std_md_link, content)
    
    return content

def process_file(input_file):
    if not os.path.exists(input_file):
        print(f"[-] Error: File '{input_file}' not found.")
        return None

    print(f"[+] Processing {input_file}...")
    
    with open(input_file, "r", encoding="utf-8") as f:
        full_content = f.read()
    
    meta, md_content = parse_frontmatter(full_content)
    # Step 0: Convert Obsidian ![[img]] embeds to standard markdown before processing
    md_content = convert_obsidian_images(md_content)
    md_content = process_images(md_content, input_file)
    
    # 1. Sanitize Secrets (Permanent File Update)
    md_content = sanitize_content(md_content, input_file)
    
    # 2. Process Obsidian Links (Ignores [[REDACTED]])
    md_content = process_obsidian_links(md_content)
    
    # Extract first image from the PROCESSED markdown
    image_pattern = r'!\[.*?\]\((.*?)\)'
    image_match = re.search(image_pattern, md_content)
    first_image = image_match.group(1) if image_match else None
    
    # 3. Convert to HTML
    html_content = convert_to_html(md_content)
    
    # 4. Apply Redaction Styles (After HTML conversion to avoid escaping issues in code blocks)
    html_content = style_redactions(html_content)
    
    if not os.path.exists(TEMPLATE_PATH):
        print(f"[-] Error: Template '{TEMPLATE_PATH}' not found.")
        return None

    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        template = f.read()
    
    filename = os.path.basename(input_file).replace(".md", ".html")
    
    # Generate SEO Tags
    seo_tags = generate_seo_tags(meta, filename, first_image)
    
    # Generate Disclaimer if needed
    # Generate Disclaimer if needed
    sensitive_cats = ["CTF", "HACKING", "SECURITY", "EXPLOIT", "MALWARE", "RED TEAM"]
    current_cat = meta.get("category", "").upper()
    current_tags = meta.get("tags", "").upper()
    
    disclaimer_html = ""
    
    # Check if any sensitive keyword is in Category OR Tags
    is_sensitive = any(cat in current_cat for cat in sensitive_cats) or \
                   any(tag in current_tags for tag in sensitive_cats)
    
    if is_sensitive:
        disclaimer_html = """
        <div class="legal-warning">
            <div class="warning-icon">⚠️ WARNING_</div>
            <p>
                <strong>DISCLAIMER:</strong> Materi ini dibuat semata-mata untuk tujuan <strong>EDUKASI</strong> dan keamanan siber.
                Penulis tidak bertanggung jawab atas segala bentuk penyalahgunaan informasi yang ada di sini.
                Menguji teknik ini pada sistem tanpa izin eksplisit adalah tindakan <strong>ILEGAL</strong>.
            </p>
        </div>
        """
    
    # Inject Metadata
    title_text = meta.get("title", "Untitled")
    
    # Dynamic Title based on sensitivity
    if is_sensitive:
        page_title = f"⚠️ | {title_text}"
    else:
        page_title = f"WRITEUP_LOG | {title_text}"
        
    output_html = template.replace("[PAGE_TITLE]", page_title)
    output_html = output_html.replace("[TITLE]", title_text) # Keep for other uses if any
    output_html = output_html.replace("[WRITEUP TITLE HERE]", title_text)
    output_html = output_html.replace("[YYYY-MM-DD]", meta.get("date", "YYYY-MM-DD"))
    output_html = output_html.replace("[WEB/NETWORK/CTF]", meta.get("category", "Uncategorized"))
    output_html = output_html.replace("[AUTHOR]", meta.get("author", "Paperalt"))
    output_html = output_html.replace("<!-- SEO_TAGS_PLACEHOLDER -->", seo_tags)
    output_html = output_html.replace("<!-- DISCLAIMER_PLACEHOLDER -->", disclaimer_html)
    
    # Inject Content
    output_html = output_html.replace("{{ CONTENT }}", html_content)
    
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    output_path = os.path.join(OUTPUT_DIR, filename)
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(output_html)
    
    print(f"[+] Successfully generated: {output_path}")
    
    # Return metadata for Sitemap/RSS
    meta['filename'] = filename
    meta['url'] = f"{BASE_URL}/writeups/{filename}"
    return meta

def generate_sitemap(posts):
    """Generates sitemap.xml"""
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    # Add root
    sitemap += f'  <url>\n    <loc>{BASE_URL}/</loc>\n    <changefreq>daily</changefreq>\n    <priority>1.0</priority>\n  </url>\n'
    
    today = datetime.date.today().strftime("%Y-%m-%d")
    
    for post in posts:
        sitemap += f'  <url>\n    <loc>{post["url"]}</loc>\n    <lastmod>{post.get("date", today)}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.8</priority>\n  </url>\n'
    
    sitemap += '</urlset>'
    
    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write(sitemap)
    print(f"[+] Generated sitemap.xml with {len(posts)} posts.")

def generate_rss(posts):
    """Generates feed.xml"""
    rss = '<?xml version="1.0" encoding="UTF-8" ?>\n'
    rss += '<rss version="2.0">\n'
    rss += '<channel>\n'
    rss += f'  <title>Paperalt Writeups</title>\n'
    rss += f'  <link>{BASE_URL}</link>\n'
    rss += f'  <description>Cyber Security Writeups & Tutorials</description>\n'
    
    for post in posts:
        rss += '  <item>\n'
        rss += f'    <title>{escape(post["title"])}</title>\n'
        rss += f'    <link>{post["url"]}</link>\n'
        rss += f'    <description>{escape(post.get("description", ""))}</description>\n'
        rss += f'    <pubDate>{post.get("date")}</pubDate>\n'
        rss += '  </item>\n'
    
    rss += '</channel>\n</rss>'
    
    with open("feed.xml", "w", encoding="utf-8") as f:
        f.write(rss)
    print(f"[+] Generated feed.xml with {len(posts)} posts.")

import json

def generate_json_index(posts):
    """Generates posts.json for client-side rendering."""
    
    # Sort posts by date (newest first)
    posts.sort(key=lambda x: x.get('date', '0000-00-00'), reverse=True)
    
    # Add ID hash if not present
    import hashlib
    for post in posts:
        if 'id' not in post:
            post['id'] = hashlib.md5(post['title'].encode()).hexdigest()[:4].upper()
            
        # Ensure relative URL
        if post['url'].startswith(BASE_URL):
            post['url'] = post['url'].replace(BASE_URL + "/", "")
            
    output_path = "posts.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(posts, f, indent=2)
        
    print(f"[+] Generated {output_path} with {len(posts)} posts.")

def generate_noscript_fallback(posts):
    """Generates static HTML links inside <noscript> for SEO."""
    
    html_output = "<h3>:: STATIC_DB_ACCESS ::</h3><ul>"
    
    # Sort by date
    posts.sort(key=lambda x: x.get('date', '0000-00-00'), reverse=True)
    
    for post in posts:
        url = post['url'].replace(BASE_URL + "/", "")
        title = post['title']
        date = post.get('date', '----')
        html_output += f'<li><a href="{url}">[{date}] {title}</a></li>\n'
    
    html_output += "</ul>"
    
    index_path = "index.html"
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        marker = "<!-- STATIC_LINKS_PLACEHOLDER -->"
        if marker in content:
            new_content = content.replace(marker, html_output)
            # Or regex replace if we already ran it, but for now simple replacement is fine 
            # as long as we don't need to update it continuously without a wrapper.
            # actually, let's use a wrapper strategy like before to be safe for re-runs.
            
            # Better strategy: Regex replace the CONTENT of <noscript>...<div class="static-list">...</div>
            # But the user asked for simple addition. 
            # To allow updates, let's replace the placeholder with "<!-- STATIC_START --> content <!-- STATIC_END -->"
            # and verify logical branching.
            
            # However, I removed the previous simpler approach. Let's just use the placeholder replacement
            # but wrapping it so we can find it again?
            # Actually, `convert.py` is often run multiple times. 
            # If I replace the placeholder, it's gone.
            # I need `<!-- STATIC_LINKS_PLACEHOLDER -->` to PERSIST or act as a boundary.
            
            pass 
            
    # Re-impl with robust replacement
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        start_marker = "<!-- STATIC_LINKS_START -->"
        end_marker = "<!-- STATIC_LINKS_END -->"
        placeholder = "<!-- STATIC_LINKS_PLACEHOLDER -->"
        
        injection = f"{start_marker}\n{html_output}\n{end_marker}"
        
        # Regex for existing block
        pattern = re.compile(f"{re.escape(start_marker)}.*?{re.escape(end_marker)}", re.DOTALL)
        
        if pattern.search(content):
            new_content = re.sub(pattern, injection, content)
            print("[+] Updated existing noscript fallback.")
        elif placeholder in content:
            new_content = content.replace(placeholder, injection)
            print("[+] Injected new noscript fallback.")
        else:
            print("[-] Warning: No placeholder found for noscript fallback.")
            return

        with open(index_path, "w", encoding="utf-8") as f:
            f.write(new_content)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 tools/convert.py <path_to_markdown_file> [more_files...]")
        sys.exit(1)
    
    posts_metadata = []
    
    for input_file in sys.argv[1:]:
        meta = process_file(input_file)
        if meta:
            posts_metadata.append(meta)
    
    # Generate Indexes
    generate_sitemap(posts_metadata)
    generate_rss(posts_metadata)
    generate_json_index(posts_metadata)
    generate_noscript_fallback(posts_metadata)

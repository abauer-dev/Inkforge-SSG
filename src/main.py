import os
import shutil
import sys
from full_md_to_html import markdown_to_html_node

def copy_files_recursive(source_dir, dest_dir):
    if not os.path.exists(source_dir):
        raise ValueError(f"Source directory does not exist: {source_dir}")

    # Wipe the destination so the copy is clean.
    # On recursive calls into subdirectories, dest_dir doesn't exist yet
    # (its parent was just created above it), so rmtree is skipped and
    # we just mkdir the new subdir. The deletion is only meaningful on
    # the top-level call.
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    os.mkdir(dest_dir)

    for item in os.listdir(source_dir):
        source_path = os.path.join(source_dir, item)
        dest_path = os.path.join(dest_dir, item)

        if os.path.isfile(source_path):
            print(f"  copy file: {source_path} -> {dest_path}")
            shutil.copy(source_path, dest_path)
        else:
            print(f"  enter dir: {source_path} -> {dest_path}")
            copy_files_recursive(source_path, dest_path)

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise ValueError("no h1 for title found")

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    with open(from_path) as f:
        markdown = f.read()
    with open(template_path) as t:
        template = t.read()
    content = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    page = template.replace("{{ Content }}", content).replace("{{ Title }}", title).replace('href="', f'href="{basepath}').replace('src="', f'src="{basepath}')

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as d:
        d.write(page)
    
def generate_pages_recursive(content_dir, template_path, dest_dir, basepath):
    for entry in os.listdir(content_dir):
        content_path = os.path.join(content_dir, entry)
        dest_path = os.path.join(dest_dir, entry)

        if os.path.isfile(content_path):
            if content_path.endswith(".md"):
                dest_path = dest_path[:-3] + ".html"
                generate_page(content_path, template_path, dest_path, basepath)
        else:
            generate_pages_recursive(content_path, template_path, dest_path, basepath)


def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    copy_files_recursive("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)
    #generate_page("content/index.md", "template.html", "public/index.html")

main()
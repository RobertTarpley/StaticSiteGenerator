import os
import shutil
import sys
# Add the src directory to the path so we can import modules
sys.path.append(os.path.dirname(__file__))

from textnode import TextNode, TextType, markdown_to_html_node, extract_title

def copy_static_to_public(source_dir="static", dest_dir="docs"):
    """
    Recursively copies all contents from source directory to destination directory.
    Deletes destination directory contents first to ensure clean copy.
    """
    print(f"Starting copy from {source_dir} to {dest_dir}")
    
    # Check if source directory exists
    if not os.path.exists(source_dir):
        print(f"Source directory {source_dir} does not exist")
        return
    
    # Delete destination directory if it exists to ensure clean copy
    if os.path.exists(dest_dir):
        print(f"Removing existing {dest_dir} directory")
        shutil.rmtree(dest_dir)
    
    # Create destination directory
    print(f"Creating {dest_dir} directory")
    os.mkdir(dest_dir)
    
    # Copy all contents recursively
    copy_directory_contents(source_dir, dest_dir)
    print(f"Finished copying from {source_dir} to {dest_dir}")

def copy_directory_contents(source_dir, dest_dir):
    """
    Recursively copies all files and subdirectories from source to destination.
    """
    # List all items in source directory
    items = os.listdir(source_dir)
    
    for item in items:
        source_path = os.path.join(source_dir, item)
        dest_path = os.path.join(dest_dir, item)
        
        if os.path.isfile(source_path):
            # Copy file and log the operation
            print(f"Copying file: {source_path} -> {dest_path}")
            shutil.copy(source_path, dest_path)
        else:
            # It's a directory - create it in destination and recurse
            print(f"Creating directory: {dest_path}")
            os.mkdir(dest_path)
            copy_directory_contents(source_path, dest_path)

def generate_page(from_path, template_path, dest_path, basepath="/"):
    """
    Generates an HTML page from a markdown file using a template.
    """
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    # Read the markdown file
    with open(from_path, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    
    # Read the template file
    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()
    
    # Convert markdown to HTML
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()
    
    # Extract the title from markdown
    page_title = extract_title(markdown_content)
    
    # Replace placeholders in template
    final_html = template_content.replace("{{ Title }}", page_title)
    final_html = final_html.replace("{{ Content }}", html_content)
    
    # Replace path references with basepath
    # Ensure basepath ends with / if it's not just "/"
    if basepath != "/" and not basepath.endswith("/"):
        basepath = basepath + "/"
    
    # Replace href and src attributes that start with /
    final_html = final_html.replace('href="/', f'href="{basepath}')
    final_html = final_html.replace('src="/', f'src="{basepath}')
    
    # Create destination directory if it doesn't exist
    dest_dir = os.path.dirname(dest_path)
    if dest_dir and not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    
    # Write the final HTML to destination
    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write(final_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath="/"):
    """
    Recursively generates HTML pages from all markdown files in a content directory.
    Maintains the same directory structure in the destination.
    """
    print(f"Crawling {dir_path_content} for markdown files...")
    
    # Get all entries in the content directory
    if not os.path.exists(dir_path_content):
        print(f"Content directory {dir_path_content} does not exist")
        return
    
    entries = os.listdir(dir_path_content)
    
    for entry in entries:
        entry_path = os.path.join(dir_path_content, entry)
        
        if os.path.isfile(entry_path):
            # Check if it's a markdown file
            if entry.endswith('.md'):
                # Generate corresponding HTML file path
                html_filename = entry.replace('.md', '.html')
                dest_file_path = os.path.join(dest_dir_path, html_filename)
                
                # Generate the page with basepath
                generate_page(entry_path, template_path, dest_file_path, basepath)
        else:
            # It's a directory - recurse into it
            subdest_dir = os.path.join(dest_dir_path, entry)
            generate_pages_recursive(entry_path, template_path, subdest_dir, basepath)

def main():
    # Get basepath from command line arguments, default to "/"
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
        print(f"Using basepath: {basepath}")
    else:
        print("Using default basepath: /")
    
    # Delete everything in docs directory
    if os.path.exists("docs"):
        shutil.rmtree("docs")
    
    # Copy static assets to docs directory
    copy_static_to_public()
    
    # Generate all pages recursively with basepath
    generate_pages_recursive("content", "template.html", "docs", basepath)


if __name__ == "__main__":
    main()

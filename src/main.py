import os
import shutil
import sys
import os
# Add the src directory to the path so we can import modules
sys.path.append(os.path.dirname(__file__))

from textnode import TextNode, TextType, markdown_to_html_node, extract_title

def copy_static_to_public(source_dir="static", dest_dir="public"):
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

def generate_page(from_path, template_path, dest_path):
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
    
    # Create destination directory if it doesn't exist
    dest_dir = os.path.dirname(dest_path)
    if dest_dir and not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    
    # Write the final HTML to destination
    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write(final_html)

def main():
    # Delete everything in public directory
    if os.path.exists("public"):
        shutil.rmtree("public")
    
    # Copy static assets to public directory
    copy_static_to_public()
    
    # Generate the main page
    generate_page("content/index.md", "template.html", "public/index.html")


if __name__ == "__main__":
    main()

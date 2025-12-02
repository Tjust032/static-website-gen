import os
import shutil
from block import markdown_to_html_node, extract_title

def copy_dir_contents(src, dst):
    if os.path.exists(dst):
        print(f"Deleting {dst} directory...")
        shutil.rmtree(dst)
    
    print(f"Creating {dst} directory...")
    os.mkdir(dst)
    
    # Recursive copy
    _copy_recursive(src, dst)

def _copy_recursive(src, dst):
    items = os.listdir(src)
    
    for item in items:
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)
        
        if os.path.isfile(src_path):
            # Copy the file
            print(f"Copying file: {src_path} -> {dst_path}")
            shutil.copy(src_path, dst_path)
        else:
            print(f"Creating directory: {dst_path}")
            os.mkdir(dst_path)
            _copy_recursive(src_path, dst_path)
            
def generate_page(from_path, template_path, dest_path, basepath='/'):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # Read markdown file
    with open(from_path, 'r') as f:
        md_content = f.read()

    # Read template file
    with open(template_path, 'r') as f:
        template_content = f.read()

    # Convert markdown to html
    html_node = markdown_to_html_node(md_content)
    html_content = html_node.to_html()

    title = extract_title(md_content)

    final_html = template_content.replace('{{ Title }}', title)
    final_html = final_html.replace('{{ Content }}', html_content)

    # Replace paths with basepath
    final_html = final_html.replace('href="/', f'href="{basepath}')
    final_html = final_html.replace('src="/', f'src="{basepath}')

    # Create destination directory if needed
    dest_dir = os.path.dirname(dest_path)
    if dest_dir and not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    with open(dest_path, 'w') as f:
        f.write(final_html)

    print(f"Page generated successfully at {dest_path}")

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath='/'):
    """
    Recursively crawl through the content directory and generate HTML pages
    for all markdown files found, preserving the directory structure.
    """
    items = os.listdir(dir_path_content)

    for item in items:
        src_path = os.path.join(dir_path_content, item)

        if os.path.isfile(src_path):
            # Check if it's a markdown file
            if item.endswith('.md'):
                # Convert .md to .html for the destination
                html_filename = item[:-3] + '.html'
                dest_path = os.path.join(dest_dir_path, html_filename)

                # Generate the page
                generate_page(src_path, template_path, dest_path, basepath)
        else:
            # It's a directory, recurse into it
            new_dest_dir = os.path.join(dest_dir_path, item)
            generate_pages_recursive(src_path, template_path, new_dest_dir, basepath)

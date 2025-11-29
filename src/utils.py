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
            
def generate_page(from_path, template_path, dest_path):
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
    
    # Create destination directory if needed
    dest_dir = os.path.dirname(dest_path)
    if dest_dir and not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
        
    with open(dest_path, 'w') as f:
        f.write(final_html)
    
    print(f"Page generated successfully at {dest_path}")
    
    
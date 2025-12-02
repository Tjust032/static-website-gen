import sys
from textnode import TextNode, TextType
from utils import copy_dir_contents, generate_page, generate_pages_recursive
         

def main():
    # Get basepath from CLI argument, default to '/'
    basepath = sys.argv[1] if len(sys.argv) > 1 else '/'

    copy_dir_contents("static", "docs")

    generate_pages_recursive("content", "template.html", "docs", basepath)
    
if __name__ == "__main__":
    main()
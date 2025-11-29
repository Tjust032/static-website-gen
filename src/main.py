from textnode import TextNode, TextType
from utils import copy_dir_contents, generate_page
         

def main():
    generate_page(
        "content/index.md",
        "template.html",
        "public/index.html"
    )
    
if __name__ == "__main__":
    main()
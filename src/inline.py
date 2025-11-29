from textnode import TextType, TextNode
from typing import List
import re

def split_nodes_delimiter(old_nodes: List[TextNode], delimiter: str, text_type: TextType):
    updated_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            updated_nodes.append(old_node)
        else:
            split_text = old_node.text.split(delimiter)

            # If no delimiter found, keep the original node
            if len(split_text) == 1:
                updated_nodes.append(old_node)
                continue

            # Odd number of parts means even number of delimiters (properly paired)
            if len(split_text) % 2 == 0:
                raise Exception("Invalid Markdown syntax: Unclosed delimiter")

            # Alternate between TEXT and the specified text_type
            for i, part in enumerate(split_text):
                if part == "":
                    continue
                if i % 2 == 0:
                    # Even indices are regular text
                    updated_nodes.append(TextNode(part, TextType.TEXT))
                else: 
                    # Odd indices are formatted text
                    updated_nodes.append(TextNode(part, text_type))
    return updated_nodes

def extract_markdown_images(text: str) -> List[tuple]:
    """Extract all markdown images from text. Returns list of (alt_text, url) tuples."""
    pattern = r"!\[([^\[\]]*?)\]\(([^\(\)]*?)\)"
    return re.findall(pattern, text)


def extract_markdown_links(text: str) -> List[tuple]:
    """Extract all markdown links from text. Returns list of (text, url) tuples."""
    pattern = r"(?<!!)\[([^\[\]]*?)\]\(([^\(\)]*?)\)"
    return re.findall(pattern, text)    

def split_nodes_link(old_nodes: List[TextNode]):
    split_nodes = []
    for node in old_nodes:
        link = extract_markdown_links(node.text)
        if link:
            # Get link text and URL
            link_text = link[0][0]
            link_url = link[0][1]
            
            # Find where link appears in text
            link_markdown = f"[{link_text}]({link_url})"
            parts = node.text.split(link_markdown, 1)
            if parts[0]:
                split_nodes.append(TextNode(parts[0], node.text_type))
            
            # Add the link as a link node
            split_nodes.append(TextNode(link_text, TextType.LINK, link_url))
            
            # Recursively process remaining text nodes
            if len(parts) > 1 and parts[1]:
                remaining_node = TextNode(parts[1], node.text_type)
                split_nodes.extend(split_nodes_link([remaining_node]))
        else:
            split_nodes.append(node)
    return split_nodes

def split_nodes_image(old_nodes: List[TextNode]):
    split_nodes = []
    for node in old_nodes:
        link = extract_markdown_images(node.text)
        if link:
            # Get link text and URL
            image_text = link[0][0]
            image_url = link[0][1]
            
            # Find where link appears in text
            image_markdown = f"![{image_text}]({image_url})"
            parts = node.text.split(image_markdown, 1)
            if parts[0]:
                split_nodes.append(TextNode(parts[0], node.text_type))
            
            # Add the link as a link node
            split_nodes.append(TextNode(image_text, TextType.IMG, image_url))
            
            # Recursively process remaining text nodes
            if len(parts) > 1 and parts[1]:
                remaining_node = TextNode(parts[1], node.text_type)
                split_nodes.extend(split_nodes_image([remaining_node]))
        else:
            split_nodes.append(node)
    return split_nodes

def text_to_textnodes(text: str) -> List[TextNode]:
    nodes = [TextNode(text, TextType.TEXT)]
    # First Bold
    nodes = split_nodes_delimiter(nodes, '**', TextType.BOLD)
    
    # Then Italic
    nodes = split_nodes_delimiter(nodes, '_', TextType.ITALIC)
    
    # Then Code
    nodes = split_nodes_delimiter(nodes, '`', TextType.CODE)
    
    # Then Image (special casing)
    nodes = split_nodes_image(nodes)
    
    # Then link (remainder)
    nodes = split_nodes_link(nodes)
    
    return nodes
            

def main():
    text = 'This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)'
    nodes = text_to_textnodes(text)
    print(nodes)
if __name__ == "__main__":
    main()
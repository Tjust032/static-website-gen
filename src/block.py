from enum import Enum
from htmlnode import HTMLNode, ParentNode
from inline import text_to_textnodes
from textnode import TextNode, text_node_to_html_node, TextType

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED = "unordered_list"
    ORDERED = "ordered_list"

def markdown_to_blocks(markdown):
    # Delimit by new line
    blocks = markdown.split("\n\n")
    
    filtered_blocks = []
    
    # Strip whitespace
    for block in blocks:
        block = block.strip()
        if block:
            filtered_blocks.append(block)

    return filtered_blocks


def block_to_block_type(block):
    if is_heading(block):
        return BlockType.HEADING
    elif is_code(block):
        return BlockType.CODE
    elif is_quote(block):
        return BlockType.QUOTE
    elif is_unordered(block):
        return BlockType.UNORDERED
    elif is_ordered(block):
        return BlockType.ORDERED
    else:
        return BlockType.PARAGRAPH
    

def is_heading(block):
    for level in range(1, 7):
        prefix = '#' * level + ' '
        if block.startswith(prefix):
            heading_text = block[len(prefix):].strip()
            if heading_text:
                return True
            else:
                return False
    return False

def is_code(block):
    if len(block) < 6:
        return False
    if block[0:3] == '```' and block[-3:] == '```':
        return True
    
    return False

def is_quote(block):
    lines = block.split('\n')

    for line in lines:
        if not (line.startswith('>')):
            return False
          
    return True

def is_unordered(block):
    lines = block.split('\n')

    for line in lines:
        if not (line.startswith('- ')):
            return False
        
        if not line[2:].strip():
            return False
          
    return True


def is_ordered(block):
    lines = block.split('\n')
    
    current_line = 1

    for line in lines:
        prefix = f"{current_line}. "
        
        if not (line.startswith(prefix)):
            return False
        
        # Check if there's content after prefix
        if not line[len(prefix):].strip():
            return False
          
        current_line += 1
    return True

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    
    for block in blocks:
        block_type = block_to_block_type(block)
        
        if block_type == BlockType.PARAGRAPH:
            children.append(paragraph_to_html_node(block))
        elif block_type == BlockType.HEADING:
            children.append(heading_to_html_node(block))
        elif block_type == BlockType.CODE:
            children.append(code_to_html_node(block))
        elif block_type == BlockType.QUOTE:
            children.append(quote_to_html_node(block))
        elif block_type == BlockType.UNORDERED:
            children.append(unordered_list_to_html_node(block))
        elif block_type == BlockType.ORDERED:
            children.append(ordered_list_to_html_node(block))
            
    return ParentNode(tag="div", children=children)
        
def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    
    return [text_node_to_html_node(node) for node in text_nodes]
    
def paragraph_to_html_node(block):
    text = ' '.join(block.split())
    children = text_to_children(text)
    return ParentNode(tag="p", children=children)

def heading_to_html_node(block):
    size = 0
    for char in block:
        if char == '#':
            size += 1
        else:
            break
    
    text = block[size:].strip()
    children = text_to_children(text)
    return ParentNode(tag=f"h{size}", children=children)
    
def code_to_html_node(block):
    code_text = block[3:-3]
    
    # Remove leading newline if present
    if code_text.startswith('\n'):
        code_text = code_text[1:]
    
    # Strip leading whitespace from each line while preserving the structure
    lines = code_text.split('\n')
    stripped_lines = [line.strip() for line in lines]
    code_text = '\n'.join(stripped_lines)
    
    text_node = TextNode(code_text, TextType.TEXT)
    code_node = text_node_to_html_node(text_node)
    
    return ParentNode(tag="pre", children=[
        ParentNode(tag="code", children=[code_node])
    ])
    
def quote_to_html_node(block):
    lines = block.split('\n')
    stripped_lines = [line[1:].strip() for line in lines]
    text = ' '.join(stripped_lines)
    children = text_to_children(text)
    return ParentNode(tag="blockquote", children=children)

def unordered_list_to_html_node(block):
    lines = block.split('\n')
    list_items = []
    
    for line in lines:
        # remove '- ' prefix
        text = line[2:].strip()
        children = text_to_children(text)
        list_items.append(ParentNode(tag="li", children=children))
    
    return ParentNode(tag="ul", children=list_items)

def ordered_list_to_html_node(block):
    lines = block.split('\n')
    list_items = []
    
    for i, line in enumerate(lines, start=1):
        prefix = f"{i}. "
        text = line[len(prefix):].strip()
        children = text_to_children(text)
        list_items.append(ParentNode(tag="li", children=children))
        
    return ParentNode(tag="ol", children=list_items)


def extract_title(markdown):
    lines = markdown.split('\n')
    
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('# ') and not stripped.startswith('## '):
            # Extract the title text after "# "
            return stripped[2:].strip()
    
    raise Exception("No h1 header")
    
    

def main():
        print(extract_title("# Hello"))

if __name__ == "__main__":
    main()
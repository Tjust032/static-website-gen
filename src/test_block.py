import unittest
from block import markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node


class TestSplitNodesDelimiter(unittest.TestCase):

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
      
    def test_heading_levels(self):
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("## Heading 2"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("### Heading 3"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("#### Heading 4"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("##### Heading 5"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)
    
    def test_heading_invalid(self):
        self.assertEqual(block_to_block_type("####### Too many"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("#No space"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("# "), BlockType.PARAGRAPH)
    
    def test_code_block(self):
        self.assertEqual(block_to_block_type("```\ncode here\n```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("```python\nprint('hello')\n```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("```\n```"), BlockType.CODE)
    
    def test_code_block_invalid(self):
        self.assertEqual(block_to_block_type("```\nno closing"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("no opening\n```"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("``code``"), BlockType.PARAGRAPH)
    
    def test_quote_block(self):
        self.assertEqual(block_to_block_type(">quote"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(">line 1\n>line 2"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(">line 1\n>line 2\n>line 3"), BlockType.QUOTE)
    
    def test_quote_block_invalid(self):
        self.assertEqual(block_to_block_type(">line 1\nline 2"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("line 1\n>line 2"), BlockType.PARAGRAPH)
    
    def test_unordered_list(self):
        self.assertEqual(block_to_block_type("- item 1"), BlockType.UNORDERED)
        self.assertEqual(block_to_block_type("- item 1\n- item 2"), BlockType.UNORDERED)
        self.assertEqual(block_to_block_type("- item 1\n- item 2\n- item 3"), BlockType.UNORDERED)
    
    def test_unordered_list_invalid(self):
        self.assertEqual(block_to_block_type("-no space"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("- item 1\nitem 2"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("- "), BlockType.PARAGRAPH)
    
    def test_ordered_list(self):
        self.assertEqual(block_to_block_type("1. item 1"), BlockType.ORDERED)
        self.assertEqual(block_to_block_type("1. item 1\n2. item 2"), BlockType.ORDERED)
        self.assertEqual(block_to_block_type("1. item 1\n2. item 2\n3. item 3"), BlockType.ORDERED)
    
    def test_ordered_list_invalid(self):
        self.assertEqual(block_to_block_type("2. item 1"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("1. item 1\n3. item 3"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("1.no space"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("1. "), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("1. item 1\n2. item 2\nitem 3"), BlockType.PARAGRAPH)
    
    def test_paragraph(self):
        self.assertEqual(block_to_block_type("Just normal text"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("Text with **bold**"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("Multiple lines\nof text"), BlockType.PARAGRAPH)
        
    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )


if __name__ == "__main__":
    unittest.main()

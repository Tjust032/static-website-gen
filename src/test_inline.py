import unittest
from textnode import TextNode, TextType
from inline import split_nodes_delimiter, extract_markdown_images, split_nodes_image, split_nodes_link


class TestSplitNodesDelimiter(unittest.TestCase):

    def test_split_delimiter_bold(self):
        """Core functionality with a typical case"""
        node = TextNode("This is text with a **bolded phrase** in the middle", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bolded phrase", TextType.BOLD),
            TextNode(" in the middle", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_delimiter_multiple_bold(self):
        """Tests multiple occurrences (common real-world scenario)"""
        node = TextNode("This **first** and **second** are bold", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This ", TextType.TEXT),
            TextNode("first", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("second", TextType.BOLD),
            TextNode(" are bold", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_delimiter_not_closed(self):
        """Error handling for malformed input"""
        node = TextNode("This has an opening **bold but no closing", TextType.TEXT)
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertIn("Invalid Markdown syntax", str(context.exception))

    def test_split_delimiter_start_end(self):
        """Edge case coverage (delimiters at boundaries)"""
        # Test delimiter at start
        node_start = TextNode("**bold** text here", TextType.TEXT)
        new_nodes_start = split_nodes_delimiter([node_start], "**", TextType.BOLD)
        expected_start = [
            TextNode("bold", TextType.BOLD),
            TextNode(" text here", TextType.TEXT),
        ]
        self.assertEqual(new_nodes_start, expected_start)

        # Test delimiter at end
        node_end = TextNode("text here **bold**", TextType.TEXT)
        new_nodes_end = split_nodes_delimiter([node_end], "**", TextType.BOLD)
        expected_end = [
            TextNode("text here ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
        ]
        self.assertEqual(new_nodes_end, expected_end)

    def test_split_delimiter_preserves_non_text(self):
        """Ensures your function doesn't break existing node types"""
        nodes = [
            TextNode("Text with **bold** here", TextType.TEXT),
            TextNode("Already italic", TextType.ITALIC),
            TextNode("More **bold** text", TextType.TEXT),
        ]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" here", TextType.TEXT),
            TextNode("Already italic", TextType.ITALIC),
            TextNode("More ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)
        
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
        
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMG, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMG, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    def test_split_links(self):
        node = TextNode(
            "This is hyperlinked [text](https://google.com) with an [link](https://i.imgur.com/zjjcJKZ.png) and another [third link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
            TextNode("This is hyperlinked ", TextType.TEXT),
            TextNode("text", TextType.LINK, "https://google.com"),
            TextNode(" with an ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("third link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

if __name__ == "__main__":
    unittest.main()

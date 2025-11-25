import unittest

from htmlnode import HTMLNode, LeafNode

class TestTextNode(unittest.TestCase):
    def test_props_to_html(self):
        node_props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node = HTMLNode("p", "Hey man", children=None, props=node_props)

        expected_str = 'href="https://www.google.com" target="_blank"'
        self.assertEqual(expected_str, node.props_to_html())

    def test_props_to_html_empty(self):
        node = HTMLNode("div", "Content", children=None, props=None)
        self.assertEqual("", node.props_to_html())

    def test_props_to_html_single_prop(self):
        node_props = {"class": "container"}
        node = HTMLNode("div", "Content", children=None, props=node_props)
        self.assertEqual('class="container"', node.props_to_html())

    def test_repr(self):
        node_props = {"href": "https://www.google.com", "target": "_blank"}
        node = HTMLNode("a", "Click me", children=None, props=node_props)
        self.assertEqual(
            repr(node),
            "HTMLNode(tag=a, value=Click me, children=None, props={'href': 'https://www.google.com', 'target': '_blank'})"
        )
    
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_repr(self):
        node_props = {"href": "https://www.google.com", "target": "_blank"}
        node = LeafNode("a", "Click me!", props=node_props)
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com" target="_blank">Click me!</a>'
        )

if __name__ == "__main__":
    unittest.main()
        
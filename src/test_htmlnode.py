import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHtmlNode(unittest.TestCase):
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
        
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")
        
    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
        
    def test_to_html_no_children(self):
        parent_node = ParentNode("div", None)
        
        with self.assertRaises(ValueError) as cm:
            parent_node.to_html()
        self.assertEqual(str(cm.exception), "No children in parent node")
    
if __name__ == "__main__":
    unittest.main()
        
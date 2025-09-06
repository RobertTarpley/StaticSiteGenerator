import unittest

from htmlnode import HtmlNode

class HtmlNodeTest(unittest.TestCase):
    def test_create_simple_html_node(self):
        text_node = HtmlNode(tag_name="p", value="Hello, World!", props={"class": "intro"})
        self.assertEqual(text_node.tag_name, "p")
        self.assertEqual(text_node.value, "Hello, World!")
        self.assertEqual(text_node.children, [])
        self.assertEqual(text_node.props, {"class": "intro"})

    def test_create_html_node_without_properties(self):
        no_props_node = HtmlNode(tag_name="div", value="Some content")
        self.assertEqual(no_props_node.tag_name, "div")
        self.assertEqual(no_props_node.value, "Some content")
        self.assertEqual(no_props_node.children, [])
        self.assertEqual(no_props_node.props, {})

    def test_prop_to_html_empty(self):
        node = HtmlNode(tag_name="div")
        expected_output = ""
        self.assertEqual(node.props_to_html(), expected_output)

    def test_props_to_html_single_propr(self):
        node = HtmlNode(tag_name="a", props={"href": "https://example.com"})
        expected_output = ' href="https://example.com"'
        self.assertEqual(node.props_to_html(), expected_output)

    def test_props_to_html_multiple_props(self):
        node = HtmlNode(tag_name="img", props={"src": "image.jpg", "alt": "Sample Image"})
        expected_output = ' src="image.jpg" alt="Sample Image"'
        self.assertEqual(node.props_to_html(), expected_output)

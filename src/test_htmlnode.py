import unittest

from htmlnode import HtmlNode, LeafNode, ParentNode

class HtmlNodeTest(unittest.TestCase):
    # ===== HtmlNode Base Class Tests =====
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

    # ===== LeafNode Tests =====
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_img(self):
        node = LeafNode("img", "", {"src": "image.jpg", "alt": "Sample Image"})
        self.assertEqual(node.to_html(), '<img src="image.jpg" alt="Sample Image"></img>')

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://example.com"})
        self.assertEqual(node.to_html(), '<a href="https://example.com">Click me!</a>')

    def test_leaf_to_html_span(self):
        node = LeafNode("span", "Highlighted text", {"class": "highlight"})
        self.assertEqual(node.to_html(), '<span class="highlight">Highlighted text</span>')

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Raw text content")
        self.assertEqual(node.to_html(), "Raw text content")

    def test_leaf_to_html_no_props(self):
        node = LeafNode("h1", "Main Title")
        self.assertEqual(node.to_html(), "<h1>Main Title</h1>")

    def test_leaf_to_html_no_value_raises_error(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    # ===== ParentNode Tests =====
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

    def test_parent_to_html_multiple_children(self):
        child1 = LeafNode("span", "First child")
        child2 = LeafNode("p", "Second child")
        child3 = LeafNode("em", "Third child")
        parent_node = ParentNode("div", [child1, child2, child3])
        expected = "<div><span>First child</span><p>Second child</p><em>Third child</em></div>"
        self.assertEqual(parent_node.to_html(), expected)

    def test_parent_to_html_with_props(self):
        child_node = LeafNode("span", "child content")
        parent_node = ParentNode("div", [child_node], {"class": "container", "id": "main"})
        expected = '<div class="container" id="main"><span>child content</span></div>'
        self.assertEqual(parent_node.to_html(), expected)

    def test_parent_to_html_nested_parents(self):
        grandchild1 = LeafNode("strong", "bold text")
        grandchild2 = LeafNode("em", "italic text")
        child1 = ParentNode("p", [grandchild1])
        child2 = ParentNode("span", [grandchild2])
        parent = ParentNode("div", [child1, child2])
        expected = "<div><p><strong>bold text</strong></p><span><em>italic text</em></span></div>"
        self.assertEqual(parent.to_html(), expected)

    def test_parent_to_html_mixed_children(self):
        leaf_child = LeafNode("span", "leaf content")
        parent_child = ParentNode("p", [LeafNode("strong", "nested content")])
        parent_node = ParentNode("div", [leaf_child, parent_child])
        expected = "<div><span>leaf content</span><p><strong>nested content</strong></p></div>"
        self.assertEqual(parent_node.to_html(), expected)

    def test_parent_to_html_no_tag_raises_error(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError) as context:
            parent_node.to_html()
        self.assertIn("must have a tag name", str(context.exception))

    def test_parent_to_html_empty_children_raises_error(self):
        parent_node = ParentNode("div", [])
        with self.assertRaises(ValueError) as context:
            parent_node.to_html()
        self.assertIn("must have children", str(context.exception))

    def test_parent_to_html_deep_nesting(self):
        deep_child = LeafNode("span", "deep content")
        level3 = ParentNode("em", [deep_child])
        level2 = ParentNode("strong", [level3])
        level1 = ParentNode("p", [level2])
        root = ParentNode("div", [level1])
        expected = "<div><p><strong><em><span>deep content</span></em></strong></p></div>"
        self.assertEqual(root.to_html(), expected)

    def test_parent_constructor_params(self):
        child_node = LeafNode("span", "test")
        parent_node = ParentNode("div", [child_node], {"class": "test"})
        self.assertEqual(parent_node.tag_name, "div")
        self.assertEqual(parent_node.value, None)
        self.assertEqual(len(parent_node.children), 1)
        self.assertEqual(parent_node.props, {"class": "test"})

    def test_parent_constructor_no_props(self):
        child_node = LeafNode("span", "test")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.props, {})

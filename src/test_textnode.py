import unittest

from textnode import TextNode, TextType, extract_markdown_images, extract_markdown_links
from splitnodes import split_nodes_delimiter

class TestTextNode(unittest.TestCase):
    # ===== TextNode Equality Tests =====
    def test_eq_bold(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(node, node2)

    def test_ne(self):
        # Test nodes with different text types are not equal
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.ITALIC_TEXT)
        self.assertNotEqual(node, node2)

    def test_repr(self):
        # Test string representation of nodes
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(repr(node), repr(node2))

    def test_eq_url(self):
        # Test equality of link nodes
        node = TextNode("[example text](https://example.com", TextType.LINKS)
        node2 = TextNode("[example text](https://example.com", TextType.LINKS)
        self.assertEqual(node, node2)

    def test__eqimage(self):
        # Test equality of image nodes
        node = TextNode("![example image](https://example.com/image.png)", TextType.IMAGES)
        node2 = TextNode("![example image](https://example.com/image.png)", TextType.IMAGES)
        self.assertEqual(node, node2)

    def test_eq_text(self):
        # Test equality of plain text nodes
        node = TextNode("This is a text node", TextType.PLAIN_TEXT)
        node2 = TextNode("This is a text node", TextType.PLAIN_TEXT)
        self.assertEqual(node, node2)

    def test_ne_text(self):
        # Test inequality of plain text nodes with different text
        node = TextNode("This is a text node", TextType.PLAIN_TEXT)
        node2 = TextNode("This is a different text node", TextType.PLAIN_TEXT)
        self.assertNotEqual(node, node2)

    # ===== TextNode to HtmlNode Conversion Tests =====
    def test_text_to_html_plain_text(self):
        # Test conversion of plain text node (no HTML tag)
        node = TextNode("This is a text node", TextType.PLAIN_TEXT)
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag_name, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_to_html_bold(self):
        # Test conversion of bold text to <b> tag
        node = TextNode("Bold text", TextType.BOLD_TEXT)
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag_name, "b")
        self.assertEqual(html_node.value, "Bold text")
        self.assertEqual(html_node.props, {})

    def test_text_to_html_italic(self):
        # Test conversion of italic text to <i> tag
        node = TextNode("Italic text", TextType.ITALIC_TEXT)
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag_name, "i")
        self.assertEqual(html_node.value, "Italic text")
        self.assertEqual(html_node.props, {})

    def test_text_to_html_code(self):
        # Test conversion of code text to <code> tag
        node = TextNode("print('hello')", TextType.CODE_TEXT)
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag_name, "code")
        self.assertEqual(html_node.value, "print('hello')")
        self.assertEqual(html_node.props, {})

    def test_text_to_html_link(self):
        # Test conversion of link to <a> tag with href attribute
        node = TextNode("Click me!", TextType.LINKS, "https://example.com")
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag_name, "a")
        self.assertEqual(html_node.value, "Click me!")
        self.assertEqual(html_node.props, {"href": "https://example.com"})

    def test_text_to_html_image(self):
        # Test conversion of image to <img> tag with src and alt attributes
        node = TextNode("Alt text", TextType.IMAGES, "https://example.com/image.jpg")
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag_name, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://example.com/image.jpg", "alt": "Alt text"})

    def test_text_to_html_invalid_type_raises_error(self):
        # Test that invalid text type raises ValueError
        # Create a mock invalid TextType by directly setting it
        node = TextNode("Invalid", TextType.PLAIN_TEXT)
        node.text_type = "INVALID_TYPE"  # Simulate invalid type
        with self.assertRaises(ValueError) as context:
            node.text_node_to_html_node()
        self.assertIn("Unsupported text type", str(context.exception))

    # ===== Split Nodes Delimiter Tests =====
    def test_split_nodes_delimiter_code(self):
        # Test splitting code blocks with backticks
        node = TextNode("This is text with a `code block` word", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)

        expected = [
            TextNode("This is text with a ", TextType.PLAIN_TEXT),
            TextNode("code block", TextType.CODE_TEXT),
            TextNode(" word", TextType.PLAIN_TEXT)
        ]

        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[0].text_type, TextType.PLAIN_TEXT)
        self.assertEqual(new_nodes[1].text, "code block")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE_TEXT)
        self.assertEqual(new_nodes[2].text, " word")
        self.assertEqual(new_nodes[2].text_type, TextType.PLAIN_TEXT)

    def test_split_nodes_delimiter_bold(self):
        # Test splitting bold text with **
        node = TextNode("This is **bold** text", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)

        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is ")
        self.assertEqual(new_nodes[0].text_type, TextType.PLAIN_TEXT)
        self.assertEqual(new_nodes[1].text, "bold")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD_TEXT)
        self.assertEqual(new_nodes[2].text, " text")
        self.assertEqual(new_nodes[2].text_type, TextType.PLAIN_TEXT)

    def test_split_nodes_delimiter_italic(self):
        # Test splitting italic text with _
        node = TextNode("This is _italic_ text", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC_TEXT)

        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is ")
        self.assertEqual(new_nodes[0].text_type, TextType.PLAIN_TEXT)
        self.assertEqual(new_nodes[1].text, "italic")
        self.assertEqual(new_nodes[1].text_type, TextType.ITALIC_TEXT)
        self.assertEqual(new_nodes[2].text, " text")
        self.assertEqual(new_nodes[2].text_type, TextType.PLAIN_TEXT)

    def test_split_nodes_delimiter_no_delimiter(self):
        # Test node with no delimiter - should return original
        node = TextNode("This is just plain text", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)

        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "This is just plain text")
        self.assertEqual(new_nodes[0].text_type, TextType.PLAIN_TEXT)

    def test_split_nodes_delimiter_non_text_node(self):
        # Test that non-plain-text nodes are left unchanged
        node = TextNode("Already bold", TextType.BOLD_TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)

        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "Already bold")
        self.assertEqual(new_nodes[0].text_type, TextType.BOLD_TEXT)

    def test_split_nodes_delimiter_unmatched_raises_error(self):
        # Test that unmatched delimiters raise ValueError
        node = TextNode("This has unmatched `code", TextType.PLAIN_TEXT)
        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter([node], "`", TextType.CODE_TEXT)
        self.assertIn("unmatched", str(context.exception))

    # ===== Markdown Extraction Tests =====
    def test_extract_markdown_images_single(self):
        # Test extracting a single image
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        matches = extract_markdown_images(text)
        expected = [("image", "https://i.imgur.com/zjjcJKZ.png")]
        self.assertEqual(matches, expected)

    def test_extract_markdown_images_multiple(self):
        # Test extracting multiple images
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        expected = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
        ]
        self.assertEqual(matches, expected)

    def test_extract_markdown_images_none(self):
        # Test text with no images
        text = "This is just plain text with no images"
        matches = extract_markdown_images(text)
        self.assertEqual(matches, [])

    def test_extract_markdown_images_empty_alt(self):
        # Test image with empty alt text
        text = "Image with empty alt ![](https://example.com/image.jpg)"
        matches = extract_markdown_images(text)
        expected = [("", "https://example.com/image.jpg")]
        self.assertEqual(matches, expected)

    def test_extract_markdown_images_special_chars(self):
        # Test image with special characters in alt text
        text = "Special chars ![image with spaces & symbols!](https://example.com/img.png)"
        matches = extract_markdown_images(text)
        expected = [("image with spaces & symbols!", "https://example.com/img.png")]
        self.assertEqual(matches, expected)

    def test_extract_markdown_links_single(self):
        # Test extracting a single link
        text = "This is text with a link [to boot dev](https://www.boot.dev)"
        matches = extract_markdown_links(text)
        expected = [("to boot dev", "https://www.boot.dev")]
        self.assertEqual(matches, expected)

    def test_extract_markdown_links_multiple(self):
        # Test extracting multiple links
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        expected = [
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev")
        ]
        self.assertEqual(matches, expected)

    def test_extract_markdown_links_none(self):
        # Test text with no links
        text = "This is just plain text with no links"
        matches = extract_markdown_links(text)
        self.assertEqual(matches, [])

    def test_extract_markdown_links_empty_text(self):
        # Test link with empty anchor text
        text = "Empty link text [](https://example.com)"
        matches = extract_markdown_links(text)
        expected = [("", "https://example.com")]
        self.assertEqual(matches, expected)

    def test_extract_markdown_links_special_chars(self):
        # Test link with special characters in anchor text
        text = "Special chars [link with spaces & symbols!](https://example.com)"
        matches = extract_markdown_links(text)
        expected = [("link with spaces & symbols!", "https://example.com")]
        self.assertEqual(matches, expected)

    def test_extract_markdown_mixed_images_and_links(self):
        # Test text with both images and links (functions should ignore the other type)
        text = "Text with ![image](https://example.com/img.jpg) and [link](https://example.com)"
        
        image_matches = extract_markdown_images(text)
        link_matches = extract_markdown_links(text)
        
        expected_images = [("image", "https://example.com/img.jpg")]
        expected_links = [("link", "https://example.com")]
        
        self.assertEqual(image_matches, expected_images)
        self.assertEqual(link_matches, expected_links)

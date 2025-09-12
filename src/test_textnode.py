import unittest

from textnode import TextNode, TextType, extract_markdown_images, extract_markdown_links, text_to_textnodes, markdown_to_blocks, block_to_block_type, BlockType
from splitnodes import split_nodes_delimiter, split_nodes_image, split_nodes_link

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

    # ===== Split Nodes Image Tests =====
    def test_split_nodes_image_single(self):
        # Test splitting a single image from text
        node = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_image([node])

        expected = [
            TextNode("This is text with an ", TextType.PLAIN_TEXT),
            TextNode("image", TextType.IMAGES, "https://i.imgur.com/zjjcJKZ.png")
        ]

        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text, "This is text with an ")
        self.assertEqual(new_nodes[0].text_type, TextType.PLAIN_TEXT)
        self.assertEqual(new_nodes[1].text, "image")
        self.assertEqual(new_nodes[1].text_type, TextType.IMAGES)
        self.assertEqual(new_nodes[1].url, "https://i.imgur.com/zjjcJKZ.png")

    def test_split_nodes_image_multiple(self):
        # Test splitting multiple images from text
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_image([node])

        expected = [
            TextNode("This is text with an ", TextType.PLAIN_TEXT),
            TextNode("image", TextType.IMAGES, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.PLAIN_TEXT),
            TextNode("second image", TextType.IMAGES, "https://i.imgur.com/3elNhQu.png"),
        ]

        self.assertEqual(len(new_nodes), 4)
        self.assertEqual(new_nodes[0].text, "This is text with an ")
        self.assertEqual(new_nodes[0].text_type, TextType.PLAIN_TEXT)
        self.assertEqual(new_nodes[1].text, "image")
        self.assertEqual(new_nodes[1].text_type, TextType.IMAGES)
        self.assertEqual(new_nodes[1].url, "https://i.imgur.com/zjjcJKZ.png")
        self.assertEqual(new_nodes[2].text, " and another ")
        self.assertEqual(new_nodes[2].text_type, TextType.PLAIN_TEXT)
        self.assertEqual(new_nodes[3].text, "second image")
        self.assertEqual(new_nodes[3].text_type, TextType.IMAGES)
        self.assertEqual(new_nodes[3].url, "https://i.imgur.com/3elNhQu.png")

    def test_split_nodes_image_no_images(self):
        # Test text with no images - should return original node
        node = TextNode("This is just plain text with no images", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_image([node])

        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "This is just plain text with no images")
        self.assertEqual(new_nodes[0].text_type, TextType.PLAIN_TEXT)

    def test_split_nodes_image_non_text_node(self):
        # Test that non-plain-text nodes are left unchanged
        node = TextNode("Already bold", TextType.BOLD_TEXT)
        new_nodes = split_nodes_image([node])

        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "Already bold")
        self.assertEqual(new_nodes[0].text_type, TextType.BOLD_TEXT)

    def test_split_nodes_image_only_image(self):
        # Test text that is only an image (no surrounding text)
        node = TextNode("![image](https://example.com/image.jpg)", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_image([node])

        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "image")
        self.assertEqual(new_nodes[0].text_type, TextType.IMAGES)
        self.assertEqual(new_nodes[0].url, "https://example.com/image.jpg")

    def test_split_nodes_image_empty_alt_text(self):
        # Test image with empty alt text
        node = TextNode("Text with ![](https://example.com/image.jpg) empty alt", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_image([node])

        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "Text with ")
        self.assertEqual(new_nodes[0].text_type, TextType.PLAIN_TEXT)
        self.assertEqual(new_nodes[1].text, "")
        self.assertEqual(new_nodes[1].text_type, TextType.IMAGES)
        self.assertEqual(new_nodes[1].url, "https://example.com/image.jpg")
        self.assertEqual(new_nodes[2].text, " empty alt")
        self.assertEqual(new_nodes[2].text_type, TextType.PLAIN_TEXT)

    # ===== Split Nodes Link Tests =====
    def test_split_nodes_link_single(self):
        # Test splitting a single link from text
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev)", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_link([node])

        expected = [
            TextNode("This is text with a link ", TextType.PLAIN_TEXT),
            TextNode("to boot dev", TextType.LINKS, "https://www.boot.dev")
        ]

        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text, "This is text with a link ")
        self.assertEqual(new_nodes[0].text_type, TextType.PLAIN_TEXT)
        self.assertEqual(new_nodes[1].text, "to boot dev")
        self.assertEqual(new_nodes[1].text_type, TextType.LINKS)
        self.assertEqual(new_nodes[1].url, "https://www.boot.dev")

    def test_split_nodes_link_multiple(self):
        # Test splitting multiple links from text (matches requirements example)
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_link([node])

        expected = [
            TextNode("This is text with a link ", TextType.PLAIN_TEXT),
            TextNode("to boot dev", TextType.LINKS, "https://www.boot.dev"),
            TextNode(" and ", TextType.PLAIN_TEXT),
            TextNode("to youtube", TextType.LINKS, "https://www.youtube.com/@bootdotdev"),
        ]

        self.assertEqual(len(new_nodes), 4)
        self.assertEqual(new_nodes[0].text, "This is text with a link ")
        self.assertEqual(new_nodes[0].text_type, TextType.PLAIN_TEXT)
        self.assertEqual(new_nodes[1].text, "to boot dev")
        self.assertEqual(new_nodes[1].text_type, TextType.LINKS)
        self.assertEqual(new_nodes[1].url, "https://www.boot.dev")
        self.assertEqual(new_nodes[2].text, " and ")
        self.assertEqual(new_nodes[2].text_type, TextType.PLAIN_TEXT)
        self.assertEqual(new_nodes[3].text, "to youtube")
        self.assertEqual(new_nodes[3].text_type, TextType.LINKS)
        self.assertEqual(new_nodes[3].url, "https://www.youtube.com/@bootdotdev")

    def test_split_nodes_link_no_links(self):
        # Test text with no links - should return original node
        node = TextNode("This is just plain text with no links", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_link([node])

        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "This is just plain text with no links")
        self.assertEqual(new_nodes[0].text_type, TextType.PLAIN_TEXT)

    def test_split_nodes_link_non_text_node(self):
        # Test that non-plain-text nodes are left unchanged
        node = TextNode("Already bold", TextType.BOLD_TEXT)
        new_nodes = split_nodes_link([node])

        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "Already bold")
        self.assertEqual(new_nodes[0].text_type, TextType.BOLD_TEXT)

    def test_split_nodes_link_only_link(self):
        # Test text that is only a link (no surrounding text)
        node = TextNode("[click here](https://example.com)", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_link([node])

        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "click here")
        self.assertEqual(new_nodes[0].text_type, TextType.LINKS)
        self.assertEqual(new_nodes[0].url, "https://example.com")

    def test_split_nodes_link_empty_anchor_text(self):
        # Test link with empty anchor text
        node = TextNode("Text with [](https://example.com) empty anchor", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_link([node])

        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "Text with ")
        self.assertEqual(new_nodes[0].text_type, TextType.PLAIN_TEXT)
        self.assertEqual(new_nodes[1].text, "")
        self.assertEqual(new_nodes[1].text_type, TextType.LINKS)
        self.assertEqual(new_nodes[1].url, "https://example.com")
        self.assertEqual(new_nodes[2].text, " empty anchor")
        self.assertEqual(new_nodes[2].text_type, TextType.PLAIN_TEXT)

    def test_split_nodes_mixed_images_and_links_ignores_other_type(self):
        # Test that split_nodes_image ignores links and split_nodes_link ignores images
        text_with_both = "Text with ![image](https://example.com/img.jpg) and [link](https://example.com)"
        node = TextNode(text_with_both, TextType.PLAIN_TEXT)

        # Test image splitting ignores links (keeps link syntax in remaining text)
        image_nodes = split_nodes_image([node])
        self.assertEqual(len(image_nodes), 3)
        self.assertEqual(image_nodes[0].text, "Text with ")
        self.assertEqual(image_nodes[0].text_type, TextType.PLAIN_TEXT)
        self.assertEqual(image_nodes[1].text, "image")
        self.assertEqual(image_nodes[1].text_type, TextType.IMAGES)
        self.assertEqual(image_nodes[1].url, "https://example.com/img.jpg")
        self.assertEqual(image_nodes[2].text, " and [link](https://example.com)")
        self.assertEqual(image_nodes[2].text_type, TextType.PLAIN_TEXT)

        # Test link splitting ignores images (keeps image syntax in remaining text)
        link_nodes = split_nodes_link([node])
        self.assertEqual(len(link_nodes), 2)
        self.assertEqual(link_nodes[0].text, "Text with ![image](https://example.com/img.jpg) and ")
        self.assertEqual(link_nodes[0].text_type, TextType.PLAIN_TEXT)
        self.assertEqual(link_nodes[1].text, "link")
        self.assertEqual(link_nodes[1].text_type, TextType.LINKS)
        self.assertEqual(link_nodes[1].url, "https://example.com")

    # ===== Text to TextNodes Tests =====
    def test_text_to_textnodes_complex_example(self):
        # Test the exact example from requirements
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)

        expected = [
            TextNode("This is ", TextType.PLAIN_TEXT),
            TextNode("text", TextType.BOLD_TEXT),
            TextNode(" with an ", TextType.PLAIN_TEXT),
            TextNode("italic", TextType.ITALIC_TEXT),
            TextNode(" word and a ", TextType.PLAIN_TEXT),
            TextNode("code block", TextType.CODE_TEXT),
            TextNode(" and an ", TextType.PLAIN_TEXT),
            TextNode("obi wan image", TextType.IMAGES, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.PLAIN_TEXT),
            TextNode("link", TextType.LINKS, "https://boot.dev"),
        ]

        self.assertEqual(len(nodes), len(expected))
        for i, (actual, expected_node) in enumerate(zip(nodes, expected)):
            self.assertEqual(actual.text, expected_node.text, f"Node {i} text mismatch")
            self.assertEqual(actual.text_type, expected_node.text_type, f"Node {i} type mismatch")
            self.assertEqual(actual.url, expected_node.url, f"Node {i} url mismatch")

    def test_text_to_textnodes_plain_text_only(self):
        # Test text with no markdown formatting
        text = "This is just plain text with no formatting"
        nodes = text_to_textnodes(text)

        expected = [TextNode("This is just plain text with no formatting", TextType.PLAIN_TEXT)]

        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text, expected[0].text)
        self.assertEqual(nodes[0].text_type, expected[0].text_type)

    def test_text_to_textnodes_bold_only(self):
        # Test text with only bold formatting
        text = "This is **bold** text"
        nodes = text_to_textnodes(text)

        expected = [
            TextNode("This is ", TextType.PLAIN_TEXT),
            TextNode("bold", TextType.BOLD_TEXT),
            TextNode(" text", TextType.PLAIN_TEXT)
        ]

        self.assertEqual(len(nodes), 3)
        for i, (actual, expected_node) in enumerate(zip(nodes, expected)):
            self.assertEqual(actual.text, expected_node.text)
            self.assertEqual(actual.text_type, expected_node.text_type)

    def test_text_to_textnodes_italic_only(self):
        # Test text with only italic formatting
        text = "This is *italic* text"
        nodes = text_to_textnodes(text)

        expected = [
            TextNode("This is ", TextType.PLAIN_TEXT),
            TextNode("italic", TextType.ITALIC_TEXT),
            TextNode(" text", TextType.PLAIN_TEXT)
        ]

        self.assertEqual(len(nodes), 3)
        for i, (actual, expected_node) in enumerate(zip(nodes, expected)):
            self.assertEqual(actual.text, expected_node.text)
            self.assertEqual(actual.text_type, expected_node.text_type)

    def test_text_to_textnodes_code_only(self):
        # Test text with only code formatting
        text = "This is `code` text"
        nodes = text_to_textnodes(text)

        expected = [
            TextNode("This is ", TextType.PLAIN_TEXT),
            TextNode("code", TextType.CODE_TEXT),
            TextNode(" text", TextType.PLAIN_TEXT)
        ]

        self.assertEqual(len(nodes), 3)
        for i, (actual, expected_node) in enumerate(zip(nodes, expected)):
            self.assertEqual(actual.text, expected_node.text)
            self.assertEqual(actual.text_type, expected_node.text_type)

    def test_text_to_textnodes_link_only(self):
        # Test text with only link
        text = "This is a [link](https://example.com)"
        nodes = text_to_textnodes(text)

        expected = [
            TextNode("This is a ", TextType.PLAIN_TEXT),
            TextNode("link", TextType.LINKS, "https://example.com")
        ]

        self.assertEqual(len(nodes), 2)
        self.assertEqual(nodes[0].text, expected[0].text)
        self.assertEqual(nodes[0].text_type, expected[0].text_type)
        self.assertEqual(nodes[1].text, expected[1].text)
        self.assertEqual(nodes[1].text_type, expected[1].text_type)
        self.assertEqual(nodes[1].url, expected[1].url)

    def test_text_to_textnodes_image_only(self):
        # Test text with only image
        text = "This is an ![image](https://example.com/image.jpg)"
        nodes = text_to_textnodes(text)

        expected = [
            TextNode("This is an ", TextType.PLAIN_TEXT),
            TextNode("image", TextType.IMAGES, "https://example.com/image.jpg")
        ]

        self.assertEqual(len(nodes), 2)
        self.assertEqual(nodes[0].text, expected[0].text)
        self.assertEqual(nodes[0].text_type, expected[0].text_type)
        self.assertEqual(nodes[1].text, expected[1].text)
        self.assertEqual(nodes[1].text_type, expected[1].text_type)
        self.assertEqual(nodes[1].url, expected[1].url)

    def test_text_to_textnodes_multiple_same_type(self):
        # Test multiple elements of the same type
        text = "This has **bold1** and **bold2** text"
        nodes = text_to_textnodes(text)

        expected = [
            TextNode("This has ", TextType.PLAIN_TEXT),
            TextNode("bold1", TextType.BOLD_TEXT),
            TextNode(" and ", TextType.PLAIN_TEXT),
            TextNode("bold2", TextType.BOLD_TEXT),
            TextNode(" text", TextType.PLAIN_TEXT)
        ]

        self.assertEqual(len(nodes), 5)
        for i, (actual, expected_node) in enumerate(zip(nodes, expected)):
            self.assertEqual(actual.text, expected_node.text)
            self.assertEqual(actual.text_type, expected_node.text_type)

    def test_text_to_textnodes_adjacent_formatting(self):
        # Test adjacent formatting elements
        text = "**bold***italic*`code`"
        nodes = text_to_textnodes(text)

        expected = [
            TextNode("bold", TextType.BOLD_TEXT),
            TextNode("italic", TextType.ITALIC_TEXT),
            TextNode("code", TextType.CODE_TEXT)
        ]

        self.assertEqual(len(nodes), 3)
        for i, (actual, expected_node) in enumerate(zip(nodes, expected)):
            self.assertEqual(actual.text, expected_node.text)
            self.assertEqual(actual.text_type, expected_node.text_type)

    def test_text_to_textnodes_mixed_images_and_links(self):
        # Test text with both images and links
        text = "Check out this ![cool image](https://example.com/img.jpg) and visit [this site](https://example.com)"
        nodes = text_to_textnodes(text)

        expected = [
            TextNode("Check out this ", TextType.PLAIN_TEXT),
            TextNode("cool image", TextType.IMAGES, "https://example.com/img.jpg"),
            TextNode(" and visit ", TextType.PLAIN_TEXT),
            TextNode("this site", TextType.LINKS, "https://example.com")
        ]

        self.assertEqual(len(nodes), 4)
        for i, (actual, expected_node) in enumerate(zip(nodes, expected)):
            self.assertEqual(actual.text, expected_node.text)
            self.assertEqual(actual.text_type, expected_node.text_type)
            self.assertEqual(actual.url, expected_node.url)

    # ===== Markdown to Blocks Tests =====
    def test_markdown_to_blocks_basic(self):
        # Test the basic example from requirements
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        expected = [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
        ]
        self.assertEqual(blocks, expected)

    def test_markdown_to_blocks_single_block(self):
        # Test markdown with just one block
        md = "This is just a single paragraph"
        blocks = markdown_to_blocks(md)
        expected = ["This is just a single paragraph"]
        self.assertEqual(blocks, expected)

    def test_markdown_to_blocks_empty_string(self):
        # Test empty markdown
        md = ""
        blocks = markdown_to_blocks(md)
        expected = []
        self.assertEqual(blocks, expected)

    def test_markdown_to_blocks_whitespace_only(self):
        # Test markdown with only whitespace
        md = "   \n\n\t  \n\n   "
        blocks = markdown_to_blocks(md)
        expected = []
        self.assertEqual(blocks, expected)

    def test_markdown_to_blocks_excessive_newlines(self):
        # Test with excessive newlines that should be filtered out
        md = """


First block


Second block



Third block


"""
        blocks = markdown_to_blocks(md)
        expected = ["First block", "Second block", "Third block"]
        self.assertEqual(blocks, expected)

    def test_markdown_to_blocks_preserves_single_newlines(self):
        # Test that single newlines within blocks are preserved
        md = """Block one
with multiple
lines

Block two
also with
multiple lines"""
        blocks = markdown_to_blocks(md)
        expected = [
            "Block one\nwith multiple\nlines",
            "Block two\nalso with\nmultiple lines"
        ]
        self.assertEqual(blocks, expected)

    def test_markdown_to_blocks_strips_whitespace(self):
        # Test that leading and trailing whitespace is stripped from blocks
        md = """   
  First block with spaces   


   Second block also with spaces   
   """
        blocks = markdown_to_blocks(md)
        expected = [
            "First block with spaces",
            "Second block also with spaces"
        ]
        self.assertEqual(blocks, expected)

    def test_markdown_to_blocks_different_block_types(self):
        # Test various markdown block types
        md = """# This is a heading

This is a paragraph of text.

## Another heading

- List item 1
- List item 2

```
code block
```

> This is a quote"""
        blocks = markdown_to_blocks(md)
        expected = [
            "# This is a heading",
            "This is a paragraph of text.",
            "## Another heading", 
            "- List item 1\n- List item 2",
            "```\ncode block\n```",
            "> This is a quote"
        ]
        self.assertEqual(blocks, expected)

    def test_markdown_to_blocks_mixed_spacing(self):
        # Test blocks with various amounts of spacing
        md = "Block1\n\nBlock2\n\n\n\nBlock3\n\n\n\n\n\nBlock4"
        blocks = markdown_to_blocks(md)
        expected = ["Block1", "Block2", "Block3", "Block4"]
        self.assertEqual(blocks, expected)

    # ===== Block to Block Type Tests =====
    def test_block_to_block_type_heading_h1(self):
        # Test heading with single # (h1)
        block = "# This is an h1 heading"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_block_to_block_type_heading_h6(self):
        # Test heading with six # characters (h6)
        block = "###### This is an h6 heading"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_block_to_block_type_heading_with_formatting(self):
        # Test heading that contains formatting markdown
        block = "## This is a heading with **bold** text"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_block_to_block_type_invalid_heading_no_space(self):
        # Test that heading without space after # is treated as paragraph
        block = "#This is not a heading"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_invalid_heading_too_many_hashes(self):
        # Test that more than 6 # characters is treated as paragraph
        block = "####### This has too many hashes"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_code_block(self):
        # Test code block with backticks
        block = "```\nprint('hello world')\nreturn 42\n```"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.CODE)

    def test_block_to_block_type_code_block_single_line(self):
        # Test single-line code block
        block = "```code here```"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.CODE)

    def test_block_to_block_type_quote_single_line(self):
        # Test single-line quote block
        block = "> This is a quote"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_block_to_block_type_quote_multi_line(self):
        # Test multi-line quote block where every line starts with >
        block = "> This is a quote\n> that spans multiple lines\n> and should be identified correctly"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_block_to_block_type_invalid_quote(self):
        # Test that block with some lines not starting with > is paragraph
        block = "> This is a quote\nThis line breaks the quote\n> Back to quote"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_unordered_list_single_item(self):
        # Test single-item unordered list
        block = "- This is a list item"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)

    def test_block_to_block_type_unordered_list_multiple_items(self):
        # Test multi-item unordered list
        block = "- First item\n- Second item\n- Third item"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)

    def test_block_to_block_type_invalid_unordered_list_no_space(self):
        # Test that list without space after - is treated as paragraph
        block = "-Not a list item\n-Another non-list"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_invalid_unordered_list_mixed(self):
        # Test that block with some lines not starting with "- " is paragraph
        block = "- This is a list item\nThis breaks the list\n- Back to list"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_ordered_list_single_item(self):
        # Test single-item ordered list
        block = "1. First item"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)

    def test_block_to_block_type_ordered_list_multiple_items(self):
        # Test multi-item ordered list with correct sequential numbering
        block = "1. First item\n2. Second item\n3. Third item\n4. Fourth item"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)

    def test_block_to_block_type_invalid_ordered_list_wrong_start(self):
        # Test that ordered list not starting with 1 is treated as paragraph
        block = "2. Second item\n3. Third item"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_invalid_ordered_list_wrong_sequence(self):
        # Test that ordered list with incorrect numbering is treated as paragraph
        block = "1. First item\n3. Third item\n4. Fourth item"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_invalid_ordered_list_no_space(self):
        # Test that ordered list without space after number is treated as paragraph
        block = "1.First item\n2.Second item"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_paragraph_simple(self):
        # Test simple paragraph text
        block = "This is just a regular paragraph of text."
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_paragraph_with_formatting(self):
        # Test paragraph containing inline formatting
        block = "This is a paragraph with **bold** and *italic* text."
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_paragraph_multiline(self):
        # Test multi-line paragraph
        block = "This is a paragraph\nthat spans multiple lines\nbut is still just a paragraph"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

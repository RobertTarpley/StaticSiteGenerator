import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq_bold(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(node, node2)

    def test_ne(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.ITALIC_TEXT)
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(repr(node), repr(node2))

    def test_eq_url(self):
        node = TextNode("[example text](https://example.com", TextType.LINKS)
        node2 = TextNode("[example text](https://example.com", TextType.LINKS)
        self.assertEqual(node, node2)

    def test__eqimage(self):
        node = TextNode("![example image](https://example.com/image.png)", TextType.IMAGES)
        node2 = TextNode("![example image](https://example.com/image.png)", TextType.IMAGES)
        self.assertEqual(node, node2)

    def test_eq_text(self):
        node = TextNode("This is a text node", TextType.PLAIN_TEXT)
        node2 = TextNode("This is a text node", TextType.PLAIN_TEXT)
        self.assertEqual(node, node2)

    def test_ne_text(self):
        node = TextNode("This is a text node", TextType.PLAIN_TEXT)
        node2 = TextNode("This is a different text node", TextType.PLAIN_TEXT)
        self.assertNotEqual(node, node2)

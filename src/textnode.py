from enum import Enum
from htmlnode import LeafNode
import re


def extract_markdown_images(text):
    """Extracts images from markdown text and returns list of (alt_text, url) tuples."""
    # Pattern matches ![alt text](url)
    pattern = r'!\[([^\[\]]*?)\]\(([^\(\)]*?)\)'
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_links(text):
    """extracts markdown links instead of images. It should return tuples of anchor text and URLs"""
    # Pattern matches [text](url) but NOT ![text](url)
    pattern = r'(?<!\!)\[([^\[\]]*?)\]\(([^\(\)]*?)\)'
    matches = re.findall(pattern, text)
    return matches


class TextType(Enum):
    PLAIN_TEXT = "text"
    BOLD_TEXT = "**Bold text**"
    ITALIC_TEXT = "_Italic text_"
    CODE_TEXT = "`Code text`"
    LINKS = "[anchor text](url)"
    IMAGES = "![alt text](url)"

class TextNode:
    def __init__(self, text, text_type=TextType.PLAIN_TEXT, url = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return False
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text!r}, {self.text_type.value!r}, {self.url!r})"

    def text_node_to_html_node(self):
        if self.text_type == TextType.PLAIN_TEXT :
            return LeafNode(None, self.text)
        if self.text_type == TextType.BOLD_TEXT :
            return LeafNode("b", self.text)
        if self.text_type == TextType.ITALIC_TEXT :
            return LeafNode("i", self.text)
        if self.text_type == TextType.CODE_TEXT :
            return LeafNode("code", self.text)
        if self.text_type == TextType.LINKS :
            return LeafNode("a", self.text, {"href": self.url})
        if self.text_type == TextType.IMAGES :
            return LeafNode("img", "", {"src": self.url, "alt": self.text})
        raise ValueError(f"Unsupported text type: {self.text_type}")

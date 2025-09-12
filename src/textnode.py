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

def text_to_textnodes(text):
    """Converts markdown text into a list of TextNode objects by applying all splitting functions."""
    # Import here to avoid circular imports
    from splitnodes import split_nodes_delimiter, split_nodes_image, split_nodes_link

    # Start with the input text as a single plain text node
    nodes = [TextNode(text, TextType.PLAIN_TEXT)]

    # Apply each splitting function in sequence
    # Order matters: images first, then links, then inline formatting
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD_TEXT)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC_TEXT)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE_TEXT)

    # Filter out any empty text nodes
    nodes = [node for node in nodes if node.text != ""]

    return nodes

def markdown_to_blocks(markdown):
    blocks = []

    raw_blocks = markdown.split('\n\n')

    for block in raw_blocks:
        stripped_block = block.strip()
        if stripped_block:
            blocks.append(stripped_block)

    return blocks

def block_to_block_type(block):
    # Check for heading (1-6 # followed by space)
    if block.startswith("#"):
        count_hashes = len(block) - len(block.lstrip("#"))
        if 1 <= count_hashes <= 6 and len(block) > count_hashes and block[count_hashes] == " ":
            return BlockType.HEADING

    # Check for code block (starts and ends with ```)
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    
    # Split block into lines for multi-line checks
    lines = block.split("\n")
    
    # Check for quote block (every line starts with >)
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    
    # Check for unordered list (every line starts with "- ")
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    
    # Check for ordered list (lines start with "1. ", "2. ", etc.)
    is_ordered_list = True
    for i, line in enumerate(lines):
        expected_prefix = f"{i + 1}. "
        if not line.startswith(expected_prefix):
            is_ordered_list = False
            break
    
    if is_ordered_list and len(lines) > 0:
        return BlockType.ORDERED_LIST
    
    # Default case - it's a paragraph
    return BlockType.PARAGRAPH



class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

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

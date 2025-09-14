from enum import Enum
from htmlnode import LeafNode, ParentNode
import re
import textwrap


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
    # Process longer delimiters first to prevent conflicts (** before *)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE_TEXT)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD_TEXT)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC_TEXT)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC_TEXT)

    # Filter out any empty text nodes
    nodes = [node for node in nodes if node.text != ""]

    return nodes

def markdown_to_blocks(markdown):
    blocks = []

    # First, try to split on double newlines (traditional approach)
    raw_blocks = markdown.split('\n\n')

    for raw_block in raw_blocks:
        stripped_block = raw_block.strip()
        if not stripped_block:
            continue
            
        # Check if this block contains multiple different block types that should be split
        lines = stripped_block.split('\n')
        if len(lines) > 1:
            # Check if we need to split based on changing block types
            current_block_lines = []
            current_block_type = None
            
            i = 0
            while i < len(lines):
                line = lines[i]
                line_stripped = line.strip()
                
                if not line_stripped:
                    # Empty line within a block - add to current block
                    current_block_lines.append(line)
                    i += 1
                    continue
                
                # Determine block type of this line
                line_block_type = get_line_block_type(line_stripped)
                
                # Special handling for code blocks
                if line_stripped.startswith('```'):
                    # If we have a current block, finalize it
                    if current_block_lines:
                        blocks.append('\n'.join(current_block_lines).strip())
                        current_block_lines = []
                    
                    # Collect the entire code block (opening ``` to closing ```)
                    code_block_lines = [line]
                    i += 1
                    while i < len(lines):
                        code_block_lines.append(lines[i])
                        if lines[i].strip().endswith('```'):
                            break
                        i += 1
                    
                    # Add the complete code block
                    blocks.append('\n'.join(code_block_lines).strip())
                    current_block_lines = []
                    current_block_type = None
                    i += 1
                    continue
                
                # If block type changes, split here
                if (current_block_type and 
                    current_block_type != line_block_type):
                    # Finalize current block
                    if current_block_lines:
                        blocks.append('\n'.join(current_block_lines).strip())
                        current_block_lines = []
                
                current_block_lines.append(line)
                current_block_type = line_block_type
                i += 1
            
            # Add the final block
            if current_block_lines:
                blocks.append('\n'.join(current_block_lines).strip())
        else:
            # Single line block, add as-is
            blocks.append(stripped_block)

    return blocks

def get_line_block_type(line):
    """Helper function to determine the block type of a single line."""
    # Check for heading
    if line.startswith('#'):
        count_hashes = len(line) - len(line.lstrip('#'))
        if 1 <= count_hashes <= 6 and len(line) > count_hashes and line[count_hashes] == ' ':
            return BlockType.HEADING
    
    # Check for code block
    if line.startswith('```'):
        return BlockType.CODE
    
    # Check for quote
    if line.startswith('>'):
        return BlockType.QUOTE
    
    # Check for unordered list
    if line.startswith('- '):
        return BlockType.UNORDERED_LIST
    
    # Check for ordered list
    if '.' in line and line.split('.')[0].isdigit() and line.startswith(line.split('.')[0] + '. '):
        return BlockType.ORDERED_LIST
    
    # Default to paragraph
    return BlockType.PARAGRAPH

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

def text_to_children(text, exclude_delimiters=None):
    """Converts text with inline markdown to list of HTMLNode children."""
    if exclude_delimiters is None:
        exclude_delimiters = set()
    
    text_nodes = text_to_textnodes_selective(text, exclude_delimiters)
    children = []
    for text_node in text_nodes:
        if text_node.text_type == TextType.BOLD_TEXT:
            # Process the content inside the bold text, but exclude bold delimiter to prevent infinite recursion
            nested_children = text_to_children(text_node.text, exclude_delimiters | {"**"})
            children.append(ParentNode("b", nested_children))
        elif text_node.text_type == TextType.ITALIC_TEXT:
            # Process the content inside the italic text, but exclude italic delimiters
            nested_children = text_to_children(text_node.text, exclude_delimiters | {"*", "_"})
            children.append(ParentNode("i", nested_children))
        else:
            # For other types, use regular conversion
            html_node = text_node.text_node_to_html_node()
            children.append(html_node)
    return children

def text_to_textnodes_selective(text, exclude_delimiters=None):
    """Like text_to_textnodes but can exclude certain delimiters to prevent infinite recursion."""
    if exclude_delimiters is None:
        exclude_delimiters = set()
        
    # Import here to avoid circular imports
    from splitnodes import split_nodes_delimiter, split_nodes_image, split_nodes_link

    # Start with the input text as a single plain text node
    nodes = [TextNode(text, TextType.PLAIN_TEXT)]

    # Apply splitting functions, but skip excluded delimiters
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    
    if "`" not in exclude_delimiters:
        nodes = split_nodes_delimiter(nodes, "`", TextType.CODE_TEXT)
    if "**" not in exclude_delimiters:
        nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD_TEXT)
    if "*" not in exclude_delimiters:
        nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC_TEXT)
    if "_" not in exclude_delimiters:
        nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC_TEXT)

    # Filter out any empty text nodes
    nodes = [node for node in nodes if node.text != ""]

    return nodes

def extract_title(markdown):
    """
    Extracts the h1 header from markdown text.
    Returns the header text without the # and leading/trailing whitespace.
    Raises an exception if no h1 header is found.
    """
    lines = markdown.split('\n')
    
    for line in lines:
        # Check if line contains an h1 header (# followed by space or just #)
        stripped_line = line.strip()
        if stripped_line.startswith('#') and not stripped_line.startswith('##'):
            # Look at the original line to see if there was a space after #
            line_after_hash = line.lstrip()  # Remove leading whitespace but keep trailing
            if len(line_after_hash) > 1 and line_after_hash[1] == ' ':
                # Extract title by removing the "# " and stripping whitespace  
                title = line_after_hash[2:].strip()
                return title
    
    # If we get here, no h1 header was found
    raise ValueError("No h1 header found in markdown")

def markdown_to_html_node(markdown):
    """Converts a full markdown document into a single parent HTMLNode."""
    # Split markdown into blocks
    blocks = markdown_to_blocks(markdown)
    
    # Convert each block to an HTMLNode
    block_nodes = []
    
    for block in blocks:
        block_type = block_to_block_type(block)
        
        if block_type == BlockType.PARAGRAPH:
            # Create paragraph node with inline formatting
            # Replace newlines with spaces and normalize whitespace
            paragraph_text = block.replace("\n", " ")
            # Replace multiple spaces with single spaces
            paragraph_text = re.sub(r'\s+', ' ', paragraph_text).strip()
            children = text_to_children(paragraph_text)
            block_nodes.append(ParentNode("p", children))
            
        elif block_type == BlockType.HEADING:
            # Determine heading level from number of # characters
            level = len(block) - len(block.lstrip("#"))
            heading_text = block[level + 1:]  # Remove "# " prefix
            children = text_to_children(heading_text)
            block_nodes.append(ParentNode(f"h{level}", children))
            
        elif block_type == BlockType.CODE:
            # Code blocks don't process inline markdown
            code_text = block[3:-3]  # Remove ``` from start and end
            
            # Use textwrap.dedent to remove common leading whitespace
            # Strip leading newline but preserve trailing newline if it exists
            code_text = textwrap.dedent(code_text)
            if code_text.startswith('\n'):
                code_text = code_text[1:]
            
            code_node = TextNode(code_text, TextType.PLAIN_TEXT)
            html_node = code_node.text_node_to_html_node()
            block_nodes.append(ParentNode("pre", [ParentNode("code", [html_node])]))
            
        elif block_type == BlockType.QUOTE:
            # Remove > from each line and process inline markdown
            lines = block.split("\n")
            quote_text = "\n".join(line[1:].lstrip() for line in lines)  # Remove > and leading space
            children = text_to_children(quote_text)
            block_nodes.append(ParentNode("blockquote", children))
            
        elif block_type == BlockType.UNORDERED_LIST:
            # Create list items for each line
            lines = block.split("\n")
            list_items = []
            for line in lines:
                item_text = line[2:]  # Remove "- "
                item_children = text_to_children(item_text)
                list_items.append(ParentNode("li", item_children))
            block_nodes.append(ParentNode("ul", list_items))
            
        elif block_type == BlockType.ORDERED_LIST:
            # Create list items for each line
            lines = block.split("\n")
            list_items = []
            for line in lines:
                # Find the first space after the number and period
                space_index = line.find(" ")
                item_text = line[space_index + 1:]  # Remove "1. ", "2. ", etc.
                item_children = text_to_children(item_text)
                list_items.append(ParentNode("li", item_children))
            block_nodes.append(ParentNode("ol", list_items))
    
    # Wrap everything in a div (handle empty case)
    if not block_nodes:
        # For empty documents, create a div with empty text node
        empty_node = TextNode("", TextType.PLAIN_TEXT).text_node_to_html_node()
        return ParentNode("div", [empty_node])
    
    return ParentNode("div", block_nodes)



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

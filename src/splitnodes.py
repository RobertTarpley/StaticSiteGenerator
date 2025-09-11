from textnode import TextNode, TextType, extract_markdown_images, extract_markdown_links

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.PLAIN_TEXT:
            new_nodes.append(node)
            continue

        split_text = node.text.split(delimiter)

        if len(split_text) == 1:
            new_nodes.append(node)
            continue

        if len(split_text) % 2 == 0:
            raise ValueError(f"Invalid markdown: unmatched {delimiter} delimiter")

        for i, part in enumerate(split_text):
            if part == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.PLAIN_TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))

    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []
    
    for node in old_nodes:
        if node.text_type != TextType.PLAIN_TEXT:
            new_nodes.append(node)
            continue
            
        images = extract_markdown_images(node.text)
        if not images:
            new_nodes.append(node)
            continue
            
        current_text = node.text
        for alt_text, url in images:
            # Find the full markdown image syntax
            full_image = f"![{alt_text}]({url})"
            parts = current_text.split(full_image, 1)
            
            if len(parts) != 2:
                continue
                
            # Add text before image if any
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.PLAIN_TEXT))
                
            # Add image node
            new_nodes.append(TextNode(alt_text, TextType.IMAGES, url))
            
            # Continue with remaining text
            current_text = parts[1]
            
        # Add remaining text if any
        if current_text:
            new_nodes.append(TextNode(current_text, TextType.PLAIN_TEXT))
            
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    
    for node in old_nodes:
        if node.text_type != TextType.PLAIN_TEXT:
            new_nodes.append(node)
            continue
            
        links = extract_markdown_links(node.text)
        if not links:
            new_nodes.append(node)
            continue
            
        current_text = node.text
        for anchor_text, url in links:
            # Find the full markdown link syntax
            full_link = f"[{anchor_text}]({url})"
            parts = current_text.split(full_link, 1)
            
            if len(parts) != 2:
                continue
                
            # Add text before link if any
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.PLAIN_TEXT))
                
            # Add link node
            new_nodes.append(TextNode(anchor_text, TextType.LINKS, url))
            
            # Continue with remaining text
            current_text = parts[1]
            
        # Add remaining text if any
        if current_text:
            new_nodes.append(TextNode(current_text, TextType.PLAIN_TEXT))
            
    return new_nodes


def split_nodes_list(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.PLAIN_TEXT:
            new_nodes.append(node)
            continue

        split_text = node.text.split("*")
        if len(split_text) == 1:
            new_nodes.append(node)
            continue

        if len(split_text) % 2 == 0:
            raise ValueError(f"Invalid markdown: unmatched * delimiter")

        for i, part in enumerate(split_text):
            if part == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.PLAIN_TEXT))
            else:
                new_nodes.append(TextNode(part, TextType.LIST_ITEM))

    return new_nodes


def split_nodes_quote(old_nodes):
    # Placeholder function - not implemented yet
    return old_nodes

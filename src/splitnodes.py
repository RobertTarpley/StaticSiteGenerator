from textnode import TextNode, TextType

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

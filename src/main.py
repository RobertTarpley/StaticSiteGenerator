from src.textnode import TextNode, TextType

def main():
    node1 = TextNode("Hello, World!", text_type=TextType.BOLD_TEXT, url="https://example.com")
    print(node1)


if __name__ == "__main__":
    main()

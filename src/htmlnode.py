class HtmlNode:
    def __init__(self, tag_name=None, value=None, children=None, props=None):
        self.tag_name = tag_name
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}

    def to_html(self):
        raise NotImplementedError("Subclasses must implement to_html method")

    def props_to_html(self):
        props_html = ""
        for key, value in self.props.items():
            props_html += f' {key}="{value}"'
        return props_html

    def __repr__(self):
        return f"HtmlNode(tag_name={self.tag_name!r}, value={self.value!r}, children={self.children}, props={self.props})"

class LeafNode(HtmlNode):
    def __init__(self, tag_name, value, props=None):
        super().__init__(tag_name, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")

        if self.tag_name is None:
            return self.value

        return f"<{self.tag_name}{self.props_to_html()}>{self.value}</{self.tag_name}>"

class ParentNode(HtmlNode):
    def __init__(self, tag_name, children, props=None):
        super().__init__(tag_name, None, children, props)

    def to_html(self):
        if self.tag_name is None:
            raise ValueError("All parent nodes must have a tag name")

        if not self.children:
            raise ValueError("All parent nodes must have children")

        children_html = "".join(child.to_html() for child in self.children)
        return f"<{self.tag_name}{self.props_to_html()}>{children_html}</{self.tag_name}>"

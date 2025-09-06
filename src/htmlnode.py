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

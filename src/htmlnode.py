class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
        
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        html_str = ""
        if not self.props:
            return html_str
        
        for key in self.props:
            html_str += f'{key}="{self.props[key]}" '
        
        return html_str.rstrip()
    
    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"
    
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if not self.value:
            raise ValueError

        if not self.tag:
            return f"{self.value}"
        
        attrs = self.props_to_html()
        attrs_str = f" {attrs}" if attrs else ""
        return f"<{self.tag}{attrs_str}>{self.value}</{self.tag}>"
    
    
class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
        
    
    def to_html(self):
        raise NotImplementedError("Not implemented")
    
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
        if self.value is None:
            raise ValueError("Must have a value")

        if not self.tag:
            return f"{self.value}"

        # Self-closing tags (like img) don't need closing tags
        if self.tag == "img":
            attrs = self.props_to_html()
            attrs_str = f" {attrs}" if attrs else ""
            return f"<{self.tag}{attrs_str}>"

        attrs = self.props_to_html()
        attrs_str = f" {attrs}" if attrs else ""
        return f"<{self.tag}{attrs_str}>{self.value}</{self.tag}>"
        
class ParentNode(HTMLNode):
    
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if not self.tag:
            raise ValueError("Tag is needed")
        
        if not self.children:
            raise ValueError("No children in parent node")
        
        representation = ""
        for child in self.children:
            representation += child.to_html()
        
        return f'<{self.tag}>{representation}</{self.tag}>'  
    
    
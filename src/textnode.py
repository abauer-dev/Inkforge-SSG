from enum import Enum
from htmlnode import LeafNode
import re

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "links"
    IMAGE = "image"

class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type #TextType[text_type]
        self.url = url

    def __eq__(self, other):
        return (self.text == other.text 
        and self.text_type.value == other.text_type.value 
        and self.url == other.url)
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)    
        case TextType.BOLD:
            return LeafNode("b", text_node.text)   
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)   
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href":text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {'src':text_node.url, 'alt':text_node.text}) 
        case _:
            raise ValueError(f"Unknown text type: {text_node.text_type}")
        

## Extract MD_Elements from textnode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue
        
        elements = node.text.split(delimiter)
        if len(elements) % 2 == 0:
            raise ValueError(
                f"Invalid markdown: unmatched delimiter {delimiter!r} in {node.text!r}"
            )
        for i, element in enumerate(elements):
            if element == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(element, TextType.TEXT))
            else:
                new_nodes.append(TextNode(element, text_type))
    return new_nodes
        
def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_images(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        images = extract_markdown_images(old_node.text)
        if not images:
            new_nodes.append(old_node)
            continue

        remaining = old_node.text
        for alt, url in images:
            sections = remaining.split(f"![{alt}]({url})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown: image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))
            remaining = sections[1]

        if remaining != "":
            new_nodes.append(TextNode(remaining, TextType.TEXT))

    return new_nodes

def split_nodes_links(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        links = extract_markdown_links(old_node.text)
        if not links:
            new_nodes.append(old_node)
            continue

        remaining = old_node.text
        for text, url in links:
            sections = remaining.split(f"[{text}]({url})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown: link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(text, TextType.LINK, url))
            remaining = sections[1]

        if remaining != "":
            new_nodes.append(TextNode(remaining, TextType.TEXT))

    return new_nodes

def text_to_textnodes(text):
    init = TextNode(text, TextType.TEXT)
    first_split = split_nodes_images([init])
    second_split = split_nodes_links(first_split)
    third_split = split_nodes_delimiter(second_split, "**", TextType.BOLD)
    fourth_split = split_nodes_delimiter(third_split, "_", TextType.ITALIC)
    fith_split = split_nodes_delimiter(fourth_split, "`", TextType.CODE)

    return fith_split

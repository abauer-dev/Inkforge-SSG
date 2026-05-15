from htmlnode import LeafNode, ParentNode
from split_blocks import (
    BlockType,
    block_to_block_type,
    markdown_to_blocks,
)
from md_elements import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node


def text_to_children(text):
    """Inline markdown text -> list of LeafNode children."""
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(tn) for tn in text_nodes]


def paragraph_to_html_node(block):
    # A paragraph block may span multiple lines; collapse them with spaces
    text = " ".join(block.split("\n"))
    return ParentNode("p", text_to_children(text))


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level == 0 or level > 6:
        raise ValueError(f"Invalid heading level: {level}")
    # Skip the # chars and the required space after them
    text = block[level + 1:]
    return ParentNode(f"h{level}", text_to_children(text))


def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")
    # Strip the opening "```\n" (4 chars) and the trailing "```" (3 chars)
    text = block[4:-3]
    # Code blocks are NOT parsed for inline markdown — make one raw text node
    raw_text_node = TextNode(text, TextType.TEXT)
    code = text_node_to_html_node(raw_text_node)
    # Wrap the raw text in <code>, then the whole thing in <pre>
    return ParentNode("pre", [LeafNode("code", code.value)])


def quote_to_html_node(block):
    new_lines = []
    for line in block.split("\n"):
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        # Drop the leading ">" and any whitespace right after it
        new_lines.append(line.lstrip(">").strip())
    text = " ".join(new_lines)
    return ParentNode("blockquote", text_to_children(text))


def unordered_list_to_html_node(block):
    items = []
    for line in block.split("\n"):
        text = line[2:]  # strip "- "
        items.append(ParentNode("li", text_to_children(text)))
    return ParentNode("ul", items)


def ordered_list_to_html_node(block):
    items = []
    for line in block.split("\n"):
        # Strip everything up to and including the first ". "
        text = line[line.index(". ") + 2:]
        items.append(ParentNode("li", text_to_children(text)))
    return ParentNode("ol", items)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    if block_type == BlockType.UNORDERED_LIST:
        return unordered_list_to_html_node(block)
    if block_type == BlockType.ORDERED_LIST:
        return ordered_list_to_html_node(block)
    raise ValueError(f"Unknown block type: {block_type}")


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = [block_to_html_node(block) for block in blocks]
    return ParentNode("div", children)

def main():
    md = """
This is **bolded** paragraph
text in a p
tag here

## This is another paragraph with _italic_ text and `code` here

"""

    node = markdown_to_html_node(md)
    html = node.to_html()
    print(html)

main()
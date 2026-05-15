from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    lines = block.split("\n")

    # Heading: 1-6 # chars, then space, then text
    if re.match(r"^#{1,6} .+", block):
        return BlockType.HEADING

    # Code block: must start AND end with ```
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    # Quote: every line starts with >
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    # Unordered list: every line starts with "- "
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    # Ordered list: lines numbered 1., 2., 3., ... starting at 1
    if all(line.startswith(f"{i + 1}. ") for i, line in enumerate(lines)):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    cleaned = [block.strip() for block in blocks]
    minimal = list(filter(None, cleaned))
    return minimal

def main():
    pass
main()
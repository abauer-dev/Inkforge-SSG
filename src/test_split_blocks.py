import unittest

from split_blocks import markdown_to_blocks, block_to_block_type, BlockType

class TestSplitBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_basic(self):
        md = "# Heading\n\nThis is a paragraph.\n\n- item 1\n- item 2"
        self.assertEqual(
            markdown_to_blocks(md),
            [
                "# Heading",
                "This is a paragraph.",
                "- item 1\n- item 2",
            ],
        )

    def test_single_block(self):
        md = "Just one block of text"
        self.assertEqual(markdown_to_blocks(md), ["Just one block of text"])

    def test_empty_string(self):
        self.assertEqual(markdown_to_blocks(""), [])

    def test_only_whitespace(self):
        # Strings, die nur aus Whitespace bestehen, sollten rausfliegen
        self.assertEqual(markdown_to_blocks("   \n\n   \n\n   "), [])

    def test_excessive_blank_lines(self):
        # Mehr als zwei Newlines zwischen Blöcken — der Fall, der
        # mit strip(" ") statt strip() kaputt geht
        md = "Block 1\n\n\n\nBlock 2\n\n\nBlock 3"
        self.assertEqual(
            markdown_to_blocks(md),
            ["Block 1", "Block 2", "Block 3"],
        )

    def test_leading_and_trailing_whitespace(self):
        md = "\n\n  # Heading  \n\n  paragraph  \n\n"
        self.assertEqual(
            markdown_to_blocks(md),
            ["# Heading", "paragraph"],
        )

    def test_bullet_list_kept_together(self):
        # Newlines INNERHALB eines Blocks bleiben erhalten
        md = "- item 1\n- item 2\n- item 3"
        self.assertEqual(
            markdown_to_blocks(md),
            ["- item 1\n- item 2\n- item 3"],
        )

    def test_mixed_block_types(self):
        md = (
            "# This is a heading\n\n"
            "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.\n\n"
            "- This is the first list item in a list block\n"
            "- This is a list item\n"
            "- This is another list item"
        )
        self.assertEqual(
            markdown_to_blocks(md),
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
                "- This is the first list item in a list block\n- This is a list item\n- This is another list item",
            ],
        )

class TestBlockToBlockType(unittest.TestCase):
    def test_heading_h1(self):
        self.assertEqual(block_to_block_type("# Heading"), BlockType.HEADING)

    def test_heading_h6(self):
        self.assertEqual(block_to_block_type("###### Deep heading"), BlockType.HEADING)

    def test_too_many_hashes_is_paragraph(self):
        self.assertEqual(block_to_block_type("####### Not a heading"), BlockType.PARAGRAPH)

    def test_hash_without_space_is_paragraph(self):
        self.assertEqual(block_to_block_type("#NoSpace"), BlockType.PARAGRAPH)

    def test_code_block(self):
        block = "```\nsome code\nmore code\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_quote(self):
        block = "> line one\n> line two\n>line three"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_one_line_missing_marker(self):
        block = "> line one\nline two"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_unordered_list(self):
        block = "- item one\n- item two\n- item three"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_unordered_list_missing_space(self):
        block = "-item one\n-item two"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list(self):
        block = "1. one\n2. two\n3. three"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ordered_list_does_not_start_at_1(self):
        block = "2. two\n3. three"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_skips_a_number(self):
        block = "1. one\n2. two\n4. four"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_paragraph(self):
        self.assertEqual(
            block_to_block_type("Just some normal text."),
            BlockType.PARAGRAPH,
        )


if __name__ == "__main__":
    unittest.main()
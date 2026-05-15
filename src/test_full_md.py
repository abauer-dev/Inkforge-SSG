import unittest
from full_md_to_html import markdown_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode

class Full_md_Tests(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
    
    def test_paragraph(self):
        md = "This is a simple paragraph."
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(html, "<div><p>This is a simple paragraph.</p></div>")

    def test_paragraph_with_inline_formatting(self):
        md = "This has **bold** and _italic_ and `code` in it."
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><p>This has <b>bold</b> and <i>italic</i> and <code>code</code> in it.</p></div>",
        )

    def test_paragraph_multiline_collapses_to_one(self):
        md = "This is line one\nthis is line two\nthis is line three"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><p>This is line one this is line two this is line three</p></div>",
        )

    def test_multiple_paragraphs(self):
        md = "First paragraph.\n\nSecond paragraph."
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><p>First paragraph.</p><p>Second paragraph.</p></div>",
        )

    # ---------- Headings ----------

    def test_h1(self):
        html = markdown_to_html_node("# Heading One").to_html()
        self.assertEqual(html, "<div><h1>Heading One</h1></div>")

    def test_h6(self):
        html = markdown_to_html_node("###### Deep heading").to_html()
        self.assertEqual(html, "<div><h6>Deep heading</h6></div>")

    def test_heading_with_inline_formatting(self):
        html = markdown_to_html_node("## A **bold** heading").to_html()
        self.assertEqual(html, "<div><h2>A <b>bold</b> heading</h2></div>")

    # ---------- Code blocks ----------

    def test_code_block(self):
        md = "```\nlet x = 1\nprint(x)\n```"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><pre><code>let x = 1\nprint(x)\n</code></pre></div>",
        )

    def test_code_block_does_not_parse_inline(self):
        # The critical test: a code block should preserve ** and _ literally
        md = "```\n**not bold** and _not italic_\n```"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><pre><code>**not bold** and _not italic_\n</code></pre></div>",
        )

    # ---------- Quotes ----------

    def test_quote_single_line(self):
        html = markdown_to_html_node("> A wise quote").to_html()
        self.assertEqual(html, "<div><blockquote>A wise quote</blockquote></div>")

    def test_quote_multiline(self):
        md = "> line one\n> line two\n> line three"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><blockquote>line one line two line three</blockquote></div>",
        )

    def test_quote_with_inline_formatting(self):
        md = "> This is **very** important"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is <b>very</b> important</blockquote></div>",
        )

    # ---------- Unordered lists ----------

    def test_unordered_list(self):
        md = "- one\n- two\n- three"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><ul><li>one</li><li>two</li><li>three</li></ul></div>",
        )

    def test_unordered_list_with_inline(self):
        md = "- **bold** item\n- item with `code`\n- _italic_ item"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><ul><li><b>bold</b> item</li><li>item with <code>code</code></li><li><i>italic</i> item</li></ul></div>",
        )

    # ---------- Ordered lists ----------

    def test_ordered_list(self):
        md = "1. first\n2. second\n3. third"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><ol><li>first</li><li>second</li><li>third</li></ol></div>",
        )

    def test_ordered_list_double_digit(self):
        # Catches a bug where "10. " gets sliced as if it were "1. "
        md = "\n".join(f"{i}. item {i}" for i in range(1, 12))
        html = markdown_to_html_node(md).to_html()
        expected_items = "".join(f"<li>item {i}</li>" for i in range(1, 12))
        self.assertEqual(html, f"<div><ol>{expected_items}</ol></div>")

    # ---------- Full document ----------

    def test_full_document(self):
        md = (
            "# My Document\n\n"
            "This is a **bold** paragraph with a [link](https://boot.dev).\n\n"
            "## Section heading\n\n"
            "Here is some code:\n\n"
            "```\nprint('hello')\n```\n\n"
            "> A famous quote\n\n"
            "- list item 1\n"
            "- list item 2\n\n"
            "1. first\n"
            "2. second"
        )
        html = markdown_to_html_node(md).to_html()
        expected = (
            "<div>"
            "<h1>My Document</h1>"
            '<p>This is a <b>bold</b> paragraph with a <a href="https://boot.dev">link</a>.</p>'
            "<h2>Section heading</h2>"
            "<p>Here is some code:</p>"
            "<pre><code>print('hello')\n</code></pre>"
            "<blockquote>A famous quote</blockquote>"
            "<ul><li>list item 1</li><li>list item 2</li></ul>"
            "<ol><li>first</li><li>second</li></ol>"
            "</div>"
        )
        self.assertEqual(html, expected)

if __name__ == "__main__":
    unittest.main()

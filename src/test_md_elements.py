import unittest

from md_elements import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_images, split_nodes_links
from textnode import TextNode, TextType


class TestMdElements(unittest.TestCase):
    def test_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            result,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_bold(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            result,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_multiple_delimited_sections(self):
        node = TextNode("`a` and `b` and `c`", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            result,
            [
                TextNode("a", TextType.CODE),
                TextNode(" and ", TextType.TEXT),
                TextNode("b", TextType.CODE),
                TextNode(" and ", TextType.TEXT),
                TextNode("c", TextType.CODE),
            ],
        )

    def test_non_text_passes_through(self):
        node = TextNode("already bold", TextType.BOLD)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result, [node])

    def test_unmatched_delimiter_raises(self):
        node = TextNode("unclosed `code here", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_no_delimiter_in_text(self):
        node = TextNode("plain text", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)

class TestExtractMarkdownImages(unittest.TestCase):
    def test_basic(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(
            extract_markdown_images(text),
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
        )

    def test_single_image(self):
        text = "![alt text](https://example.com/img.png)"
        self.assertEqual(
            extract_markdown_images(text),
            [("alt text", "https://example.com/img.png")],
        )

    def test_no_images(self):
        text = "This is plain text with no images."
        self.assertEqual(extract_markdown_images(text), [])

    def test_empty_string(self):
        self.assertEqual(extract_markdown_images(""), [])

    def test_does_not_match_links(self):
        # A link starts with [ not ![ — the function must not pick this up
        text = "This is a [link](https://boot.dev), not an image"
        self.assertEqual(extract_markdown_images(text), [])

    def test_mixed_with_links(self):
        # Only the image should come out
        text = "An ![image](https://example.com/img.png) and a [link](https://boot.dev)"
        self.assertEqual(
            extract_markdown_images(text),
            [("image", "https://example.com/img.png")],
        )

    def test_empty_alt_text(self):
        text = "![](https://example.com/img.png)"
        self.assertEqual(
            extract_markdown_images(text),
            [("", "https://example.com/img.png")],
        )

    def test_image_at_start_and_end(self):
        text = "![first](https://a.com/1.png) middle ![last](https://a.com/2.png)"
        self.assertEqual(
            extract_markdown_images(text),
            [
                ("first", "https://a.com/1.png"),
                ("last", "https://a.com/2.png"),
            ],
        )

class TestExtractMarkdownLinks(unittest.TestCase):
    def test_basic(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual(
            extract_markdown_links(text),
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
        )

    def test_single_link(self):
        text = "Click [here](https://example.com)"
        self.assertEqual(
            extract_markdown_links(text),
            [("here", "https://example.com")],
        )

    def test_no_links(self):
        text = "This is plain text with no links."
        self.assertEqual(extract_markdown_links(text), [])

    def test_empty_string(self):
        self.assertEqual(extract_markdown_links(""), [])

    def test_does_not_match_images(self):
        # An image starts with ![ — this is the critical edge case.
        # If your regex is naive, it will match images as links too.
        text = "An ![image](https://example.com/img.png) is not a link"
        self.assertEqual(extract_markdown_links(text), [])

    def test_mixed_with_images(self):
        # Only the link should come out
        text = "An ![image](https://example.com/img.png) and a [link](https://boot.dev)"
        self.assertEqual(
            extract_markdown_links(text),
            [("link", "https://boot.dev")],
        )

    def test_empty_link_text(self):
        text = "[](https://example.com)"
        self.assertEqual(
            extract_markdown_links(text),
            [("", "https://example.com")],
        )

    def test_link_with_special_chars_in_url(self):
        text = "[boot dev](https://www.boot.dev/path?query=value&other=1)"
        self.assertEqual(
            extract_markdown_links(text),
            [("boot dev", "https://www.boot.dev/path?query=value&other=1")],
        )

class TestSplitNodesImage(unittest.TestCase):
    def test_basic(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/aKaOqIh.gif) in it",
            TextType.TEXT,
        )
        self.assertEqual(
            split_nodes_images([node]),
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
                TextNode(" in it", TextType.TEXT),
            ],
        )

    def test_multiple_images(self):
        node = TextNode(
            "![first](https://a.com/1.png) middle ![second](https://a.com/2.png)",
            TextType.TEXT,
        )
        self.assertEqual(
            split_nodes_images([node]),
            [
                TextNode("first", TextType.IMAGE, "https://a.com/1.png"),
                TextNode(" middle ", TextType.TEXT),
                TextNode("second", TextType.IMAGE, "https://a.com/2.png"),
            ],
        )

    def test_no_image(self):
        node = TextNode("Just plain text here", TextType.TEXT)
        self.assertEqual(split_nodes_images([node]), [node])

    def test_image_at_end(self):
        # Catches the "forgot the trailing remaining" bug
        node = TextNode(
            "Trailing text after ![img](https://a.com/x.png)",
            TextType.TEXT,
        )
        self.assertEqual(
            split_nodes_images([node]),
            [
                TextNode("Trailing text after ", TextType.TEXT),
                TextNode("img", TextType.IMAGE, "https://a.com/x.png"),
            ],
        )

    def test_image_at_start(self):
        # Catches the "emitted an empty text node" bug
        node = TextNode(
            "![img](https://a.com/x.png) and more",
            TextType.TEXT,
        )
        self.assertEqual(
            split_nodes_images([node]),
            [
                TextNode("img", TextType.IMAGE, "https://a.com/x.png"),
                TextNode(" and more", TextType.TEXT),
            ],
        )

    def test_non_text_passes_through(self):
        node = TextNode("already bold", TextType.BOLD)
        self.assertEqual(split_nodes_images([node]), [node])

    def test_ignores_links(self):
        node = TextNode("A [link](https://boot.dev) is not an image", TextType.TEXT)
        self.assertEqual(split_nodes_images([node]), [node])

class TestSplitNodesLink(unittest.TestCase):
    def test_basic(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        self.assertEqual(
            split_nodes_links([node]),
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube",
                    TextType.LINK,
                    "https://www.youtube.com/@bootdotdev",
                ),
            ],
        )

    def test_no_link(self):
        node = TextNode("Just plain text", TextType.TEXT)
        self.assertEqual(split_nodes_links([node]), [node])

    def test_link_at_end(self):
        node = TextNode("Click [here](https://boot.dev)", TextType.TEXT)
        self.assertEqual(
            split_nodes_links([node]),
            [
                TextNode("Click ", TextType.TEXT),
                TextNode("here", TextType.LINK, "https://boot.dev"),
            ],
        )

    def test_ignores_images(self):
        # The critical test — link function must not treat ![x](y) as a link
        node = TextNode("An ![img](https://a.com/x.png) here", TextType.TEXT)
        self.assertEqual(split_nodes_links([node]), [node])

    def test_non_text_passes_through(self):
        node = TextNode("already code", TextType.CODE)
        self.assertEqual(split_nodes_links([node]), [node])


if __name__ == "__main__":
    unittest.main()
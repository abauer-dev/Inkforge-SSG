import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestTextNode(unittest.TestCase):
    
    def test_default_constructor(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_constructor_with_values(self):
        node = HTMLNode("p", "Hello, world!")
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "Hello, world!")
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_constructor_all_args(self):
        child = HTMLNode("span", "child text")
        node = HTMLNode("div", "parent text", [child], {"class": "container"})
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "parent text")
        self.assertEqual(node.children, [child])
        self.assertEqual(node.props, {"class": "container"})

    def test_to_html_not_implemented(self):
        node = HTMLNode("p", "Hello")
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_props_to_html_single(self):
        node = HTMLNode("a", "Click me!", None, {"href": "https://www.boot.dev"})
        self.assertEqual(node.props_to_html(), ' href="https://www.boot.dev"')

    def test_props_to_html_multiple(self):
        node = HTMLNode(
            "a",
            "Click me!",
            None,
            {"href": "https://www.google.com", "target": "_blank"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' href="https://www.google.com" target="_blank"',
        )

    def test_props_to_html_empty(self):
        node = HTMLNode("p", "Hello", None, {})
        self.assertEqual(node.props_to_html(), "")

    def test_children_list(self):
        child1 = HTMLNode("span", "child1")
        child2 = HTMLNode("span", "child2")
        parent = HTMLNode("div", None, [child1, child2])
        self.assertEqual(len(parent.children), 2)
        self.assertEqual(parent.children[0], child1)
        self.assertEqual(parent.children[1], child2)

    def test_repr(self):
        node = HTMLNode("p", "Hello", None, {"class": "greeting"})
        self.assertEqual(
            repr(node),
            "HTMLNode(tag=p, value=Hello, children=None, props={'class': 'greeting'})",
        )

    ## Testing LeafNode

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_leaf_to_html_no_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_to_html_all(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')
    
    ## Testing ParentNode

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_to_html_with_mixed_leaf_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    # Single-child cases
    def test_to_html_single_leaf_child(self):
        node = ParentNode("div", [LeafNode("span", "hello")])
        self.assertEqual(node.to_html(), "<div><span>hello</span></div>")

    def test_to_html_single_raw_text_child(self):
        node = ParentNode("p", [LeafNode(None, "just text")])
        self.assertEqual(node.to_html(), "<p>just text</p>")

    # Nesting
    def test_to_html_with_nested_parent(self):
        child = ParentNode("span", [LeafNode("b", "deep")])
        parent = ParentNode("div", [child])
        self.assertEqual(parent.to_html(), "<div><span><b>deep</b></span></div>")

    def test_to_html_deeply_nested(self):
        innermost = LeafNode("b", "grandchild")
        middle = ParentNode("span", [innermost])
        outer = ParentNode("section", [middle])
        root = ParentNode("div", [outer])
        self.assertEqual(
            root.to_html(),
            "<div><section><span><b>grandchild</b></span></section></div>",
        )

    def test_to_html_mixed_leaf_and_parent_children(self):
        node = ParentNode(
            "div",
            [
                LeafNode("h1", "Title"),
                ParentNode("p", [LeafNode(None, "paragraph text")]),
                LeafNode(None, "trailing text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<div><h1>Title</h1><p>paragraph text</p>trailing text</div>",
        )

    # Props
    def test_to_html_with_props(self):
        node = ParentNode(
            "a",
            [LeafNode(None, "Click me")],
            {"href": "https://www.boot.dev"},
        )
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.boot.dev">Click me</a>',
        )

    def test_to_html_with_multiple_props(self):
        node = ParentNode(
            "div",
            [LeafNode(None, "content")],
            {"class": "container", "id": "main"},
        )
        self.assertEqual(
            node.to_html(),
            '<div class="container" id="main">content</div>',
        )

    def test_to_html_nested_parent_with_props(self):
        child = ParentNode(
            "a",
            [LeafNode(None, "link")],
            {"href": "https://example.com"},
        )
        parent = ParentNode("p", [LeafNode(None, "Visit "), child])
        self.assertEqual(
            parent.to_html(),
            '<p>Visit <a href="https://example.com">link</a></p>',
        )

    # Error cases
    def test_to_html_no_tag_raises(self):
        node = ParentNode(None, [LeafNode("b", "Bold")])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_no_children_raises(self):
        node = ParentNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    # Edge case: empty children list. Whether this raises or produces
    # "<p></p>" depends on your implementation choice — pick the one
    # that matches yours and delete the other.
    def test_to_html_empty_children_list(self):
        node = ParentNode("p", [])
        # Option A: empty list is valid -> empty tag pair
        self.assertEqual(node.to_html(), "<p></p>")
        # Option B: empty list is invalid -> raises
        # with self.assertRaises(ValueError):
        #     node.to_html()

    # Many siblings
    def test_to_html_many_children(self):
        children = [LeafNode("li", f"item {i}") for i in range(5)]
        node = ParentNode("ul", children)
        self.assertEqual(
            node.to_html(),
            "<ul><li>item 0</li><li>item 1</li><li>item 2</li><li>item 3</li><li>item 4</li></ul>",
        )


if __name__ == "__main__":
    unittest.main()
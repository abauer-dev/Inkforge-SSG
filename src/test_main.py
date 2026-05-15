import unittest
from main import extract_title

class test_find_title(unittest.TestCase):
    def first_test(self):
        markdown = "# My title\n\nwhy this is so good of an text"
        self.assertEqual(extract_title(markdown), "My title")

    def test_basic(self):
        md = "# Hello World"
        self.assertEqual(extract_title(md), "Hello World")

    def test_title_not_on_first_line(self):
        md = "Some intro text\n\n# The Real Title\n\nMore content"
        self.assertEqual(extract_title(md), "The Real Title")

    def test_trailing_whitespace_stripped(self):
        md = "#    Padded title   "
        self.assertEqual(extract_title(md), "Padded title")

    def test_returns_first_h1(self):
        md = "# First\n\n# Second"
        self.assertEqual(extract_title(md), "First")

    def test_no_h1_raises(self):
        md = "Just some text\n\n## Only an h2 here\n\nMore text"
        with self.assertRaises(ValueError):
            extract_title(md)

    def test_empty_string_raises(self):
        with self.assertRaises(ValueError):
            extract_title("")

    def test_h2_does_not_count(self):
        # The critical test: only "# " (one hash + space) is an h1.
        # "## " is an h2 and must NOT be picked up.
        md = "## This is h2\n### And h3"
        with self.assertRaises(ValueError):
            extract_title(md)

    def test_hash_without_space_does_not_count(self):
        md = "#NotATitle\n\nsome text"
        with self.assertRaises(ValueError):
            extract_title(md)

if __name__ == "__main__":
    unittest.main()
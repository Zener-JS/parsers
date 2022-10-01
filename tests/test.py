import unittest
from src import CSSParser


class CSSTest(unittest.TestCase):

    parent_dir = "css/"

    def css_test(self, parent_dir):
        parent_dir = self.parent_dir + parent_dir
        with open(f"{parent_dir}/in.css") as in_css, open(f"{parent_dir}/out.css") as out_css:
            self.assertEqual(CSSParser(in_css.read()).raw_css, out_css.read().strip("\n"))

    def test_comments(self):
        self.css_test("comments")

    def test_using__parser__(self):
        self.css_test("using __parser__")


if __name__ == '__main__':
    unittest.main()

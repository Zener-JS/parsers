import unittest
from src import CSSParser


class CSSTest(unittest.TestCase):

    parent_dir = "tests/css"

    def test_comments(self):
        parent_dir = self.parent_dir + "/comments"
        with open(f"{parent_dir}/in.css") as in_css, open(f"{parent_dir}/out.css") as out_css:
            self.assertEqual(CSSParser(in_css.read()).raw_css, out_css.read())


if __name__ == '__main__':
    unittest.main()

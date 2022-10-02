import unittest

from src import CSSParser
from src.css import Selector as CSSSelector
from src.css.selectors import \
    configure as css_selector_configure, \
    get_configuration as css_get_configuration,\
    new_current_selectors as css_new_current_selectors


class CSSTest(unittest.TestCase):
    parent_dir = "css/"

    def css_test(self, parent_dir):
        parent_dir = self.parent_dir + parent_dir
        with open(f"{parent_dir}/in.css") as in_css, open(f"{parent_dir}/out.css") as out_css:
            self.assertEqual(out_css.read().strip("\n"), CSSParser(in_css.read()).raw_css)

    def test_comments(self):
        self.css_test("comments")

    def test_using__parser__(self):
        self.css_test("using __parser__")

    def test_selector(self):
        selector = CSSSelector("test selector")
        selector.add_declaration("prop1", "value")
        selector.add_declaration("prop2", "value")
        with self.subTest("Test add_declaration, get_value_by_prop and get_props_by_value"):
            self.assertTrue(
                selector.get_value_by_prop("prop1") == "value" and
                selector.get_props_by_value("value") == ["prop1", "prop2"]
            )
        with self.subTest("Test prevention of overwrite in add_declaration"):
            try:
                selector.add_declaration("prop1", "overwriting value")
                self.fail("Able to overwrite prop value with add_declaration")
            except ValueError:
                pass
        with self.subTest("Test update_declaration"):
            selector.update_declaration("prop1", "another value")
            self.assertEqual("another value", selector.get_value_by_prop("prop1"))
        with self.subTest("Test prevention of adding new prop with update_declaration"):
            try:
                selector.update_declaration("A prop that does not exist", "value")
                self.fail("Able to create new prop with update_declaration")
            except ValueError:
                pass
        with self.subTest("Test delete_declaration"):
            selector.delete_declaration("prop2")
            try:
                selector.get_value_by_prop("prop2")
                self.fail("Prop not deleted")
            except ValueError:
                pass
        with self.subTest("Test checking of whether prop exists or not in delete_declaration"):
            try:
                selector.delete_declaration("A prop that does not exist")
                self.fail("No error raised")
            except ValueError:
                pass

    def test_selectors_configure(self):
        original_sq_str, original_dq_str = css_get_configuration()
        css_selector_configure("test sq str", "test dq str")
        current_configuration = css_get_configuration()
        with self.subTest("Test single quote"):
            self.assertEqual("test sq str", current_configuration[0])
        with self.subTest("Test double quote"):
            self.assertEqual("test dq str", current_configuration[1])
        css_selector_configure(original_sq_str, original_dq_str)

    def test_new_current_selectors(self):
        self.assertEqual(
            ["#test", ".test", "@test (test: \"test, test\")", "test"],
            css_new_current_selectors("#test, .test  ,@test (test: \"test, test\"),   test   ", test=True)
        )


if __name__ == '__main__':
    unittest.main()

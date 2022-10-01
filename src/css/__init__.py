"""
MIT License

Copyright (c) 2022 Jothin Kumar

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Author(s): Jothin Kumar <contact@jothin.tech>
GitHub repository: https://github.com/Zener-JS/parsers
"""


class Parser:
    def __init__(self, raw_css: str):

        # Remove leading whitespaces, trailing whitespaces, newlines
        self.raw_css = ""
        for line in raw_css.split("\n"):
            self.raw_css += line.strip()
        self.raw_css = self.raw_css.replace("\n", "")

        # CSS pre parsing
        single_quote_str = "__parser__ single-quote"
        double_quote_str = "__parser__ double-quote"
        start_comment_str = "__parser__ start_comment"
        i = 0
        while single_quote_str in self.raw_css:
            single_quote_str += str(i)
            i += 1
        i = 0
        while double_quote_str in self.raw_css:
            double_quote_str += str(i)
            i += 1
        i = 0
        while start_comment_str in self.raw_css:
            start_comment_str += str(i)
            i += 1
        self.raw_css.replace("\\\'", single_quote_str)
        self.raw_css.replace("\\\"", single_quote_str)

        # Remove comments
        while self.raw_css.partition("/*")[1] == "/*":
            partition = list(self.raw_css.partition("/*"))
            if (len(partition[0]) - len(partition[0].replace("\"", ""))) % 2 == (len(partition[0]) - len(partition[0].replace("\'", ""))) % 2 == 0:
                self.raw_css = partition[0] + partition[2].partition("*/")[2]
            else:
                if partition[1] == "/*":
                    partition[1] = start_comment_str
                self.raw_css = "".join(partition)
        self.raw_css = self.raw_css.replace(start_comment_str, "/*")

        # CSS post parsing
        self.raw_css.replace(single_quote_str, "\\\'")
        self.raw_css.replace(double_quote_str, "\\\"")

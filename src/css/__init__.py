"""
MIT License

Copyright (c) 2021 Jothin Kumar

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
        self.raw_css.replace("\\\'", "__parser__ single-quote")
        self.raw_css.replace("\\\"", "__parser__ double-quote")

        # Remove comments
        while self.raw_css.partition("/*")[1] == "/*":
            partition = list(self.raw_css.partition("/*"))
            if (len(partition[0]) - len(partition[0].replace("\"", ""))) % 2 == (len(partition[0]) - len(partition[0].replace("\'", ""))) % 2 == 0:
                self.raw_css = partition[0] + partition[2].partition("*/")[2]
            else:
                if partition[1] == "/*":
                    partition[1] = "__parser__ start-comment"
                self.raw_css = "".join(partition)
        self.raw_css = self.raw_css.replace("__parser__ start-comment", "/*")

        # CSS post parsing
        self.raw_css.replace("__parser__ single-quote", "\\\'")
        self.raw_css.replace("__parser__ double-quote", "\\\"")

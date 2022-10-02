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
single_quote_str = ""
double_quote_str = ""
selectors = list


def configure(new_single_quote_str: str, new_double_quote_str: str):
    global single_quote_str
    global double_quote_str
    single_quote_str = new_single_quote_str
    double_quote_str = new_double_quote_str


def replace__parser__(string: str):
    return string.replace(single_quote_str, "\\'").replace(double_quote_str, "\\\"")


class Selector:
    def __init__(self, selector: str):
        self.selector = replace__parser__(selector)
        self.declarations = {}

    def add_declaration(self, prop: str, value: str):
        prop, value = map(replace__parser__, [prop, value])
        if prop in self.declarations:
            raise ValueError(f"Declaration {prop} with value {value} already exists. Use update_declaration to modify it.")
        self.declarations[prop] = value

    def update_declaration(self, prop: str, new_value: str):
        prop, new_value = map(replace__parser__, [prop, new_value])
        if prop not in self.declarations:
            raise ValueError(f"Declaration {prop} does not exist. Use add_declaration to add one.")
        self.declarations[prop] = new_value

    def delete_declaration(self, prop: str):
        prop = replace__parser__(prop)
        if prop not in self.declarations:
            raise ValueError(f"Declaration {prop} does not exist.")
        del self.declarations[prop]

    def get_value_by_prop(self, prop: str):
        prop = replace__parser__(prop)
        if prop not in self.declarations:
            raise ValueError(f"Declaration {prop} does not exist.")
        return self.declarations[prop]

    def get_props_by_value(self, value: str):
        value = replace__parser__(value)
        props = []
        for prop in self.declarations:
            if self.declarations[prop] == value:
                props.append(prop)
        return props


_current_selectors = []


def new_current_selectors(new_selectors: str, test=False):
    comma_str = "__parser__ comma"
    i = 0
    while comma_str in new_selectors:
        comma_str += str(i)
        i += 1
    global _current_selectors
    _current_selectors = []
    while new_selectors:
        partition = new_selectors.partition(",")
        if (len(partition[0]) - len(partition[0].replace("\"", ""))) % 2 == (len(partition[0]) - len(partition[0].replace("\'", ""))) % 2 == 0:
            _current_selectors.append(partition[0].strip().replace(comma_str, ","))
            new_selectors = partition[2]
        else:
            new_selectors = f"{partition[0]}{comma_str}{partition[2]}"
    if test:
        return _current_selectors


def parse_declarations(declarations_str: str):
    declarations_str = declarations_str.strip()
    declarations = {}
    semicolon_str = "__parser__ semicolon"
    i = 0
    while semicolon_str in declarations_str:
        semicolon_str += str(i)
        i += 1
    while declarations_str:
        partition = declarations_str.partition(";")
        if (len(partition[0]) - len(partition[0].replace("\"", ""))) % 2 == (
                len(partition[0]) - len(partition[0].replace("\'", ""))) % 2 == 0:
            declaration = partition[0].replace(semicolon_str, ";").partition(":")
            declarations[declaration[0].strip()] = declaration[2].strip()
            declarations_str = partition[2]
        else:
            declarations_str = f"{partition[0]}{semicolon_str}{partition[2]}"
    return declarations


def get_configuration():  # For test
    return single_quote_str, double_quote_str

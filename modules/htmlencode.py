#!/usr/bin/env python
# vim: set fileencoding=UTF-8 :
"""
Code Copyright (C) 2012-2013 Liam Stanley
Credits: Sean B. Palmer, Michael Yanovich
htmlencode.py - Code Html Encode Module
http://code.liamstanley.net/
"""

import web

HTML_ENCODINGS = {
    " ":  "%20",
    "!":  "%21",
    '"':  "%22",
    "#":  "%23",
    "$":  "%24",
    "%":  "%25",
    "&":  "%26",
    "'":  "%27",
    "(":  "%28",
    ")":  "%29",
    "*":  "%2A",
    "+":  "%2B",
    ",":  "%2C",
    "-":  "%2D",
    ".":  "%2E",
    "/":  "%2F",
    ":":  "%3A",
    ";":  "%3B",
    "<":  "%3C",
    "=":  "%3D",
    ">":  "%3E",
    "?":  "%3F",
    "@":  "%40",
    "[":  "%5B",
    "\\": "%5C",
    "]":  "%5D",
    "^":  "%5E",
    "_":  "%5F",
    "`":  "%60",
    "{":  "%7B",
    "|":  "%7C",
    "}":  "%7D",
    "~":  "%7E",
    "�":  "%80",
    "�":  "%82",
    "�":  "%83",
    "�":  "%84",
    "�":  "%85",
    "�":  "%86",
    "�":  "%87",
    "�":  "%88",
    "�":  "%89",
    "�":  "%8A",
    "�":  "%8B",
    "�":  "%8C",
    "�":  "%8E",
    "�":  "%91",
    "�":  "%92",
    "�":  "%93",
    "�":  "%94",
    "�":  "%95",
    "�":  "%96",
    "�":  "%97",
    "�":  "%98",
    "�":  "%99",
    "�":  "%9A",
    "�":  "%9B",
    "�":  "%9C",
    "�":  "%9E",
    "�":  "%9F",
    "�":  "%A1",
    "�":  "%A2",
    "�":  "%A3",
    "�":  "%A5",
    "|":  "%A6",
    "�":  "%A7",
    "�":  "%A8",
    "�":  "%A9",
    "�":  "%AA",
    "�":  "%AB",
    "�":  "%AC",
    "�":  "%AD",
    "�":  "%AE",
    "�":  "%AF",
    "�":  "%B0",
    "�":  "%B1",
    "�":  "%B2",
    "�":  "%B3",
    "�":  "%B4",
    "�":  "%B5",
    "�":  "%B6",
    "�":  "%B7",
    "�":  "%B8",
    "�":  "%B9",
    "�":  "%BA",
    "�":  "%BB",
    "�":  "%BC",
    "�":  "%BD",
    "�":  "%BE",
    "�":  "%BF",
    "�":  "%C0",
    "�":  "%C1",
    "�":  "%C2",
    "�":  "%C3",
    "�":  "%C4",
    "�":  "%C5",
    "�":  "%C6",
    "�":  "%C7",
    "�":  "%C8",
    "�":  "%C9",
    "�":  "%CA",
    "�":  "%CB",
    "�":  "%CC",
    "�":  "%CD",
    "�":  "%CE",
    "�":  "%CF",
    "�":  "%D0",
    "�":  "%D1",
    "�":  "%D2",
    "�":  "%D3",
    "�":  "%D4",
    "�":  "%D5",
    "�":  "%D6",
    "�":  "%D8",
    "�":  "%D9",
    "�":  "%DA",
    "�":  "%DB",
    "�":  "%DC",
    "�":  "%DD",
    "�":  "%DE",
    "�":  "%DF",
    "�":  "%E0",
    "�":  "%E1",
    "�":  "%E2",
    "�":  "%E3",
    "�":  "%E4",
    "�":  "%E5",
    "�":  "%E6",
    "�":  "%E7",
    "�":  "%E8",
    "�":  "%E9",
    "�":  "%EA",
    "�":  "%EB",
    "�":  "%EC",
    "�":  "%ED",
    "�":  "%EE",
    "�":  "%EF",
    "�":  "%F0",
    "�":  "%F1",
    "�":  "%F2",
    "�":  "%F3",
    "�":  "%F4",
    "�":  "%F5",
    "�":  "%F6",
    "�":  "%F7",
    "�":  "%F8",
    "�":  "%F9",
    "�":  "%FA",
    "�":  "%FB",
    "�":  "%FC",
    "�":  "%FD",
    "�":  "%FE",
    "�":  "%FF",
}

uri = "http://www.numberempire.com/equation.render?"

def latex(code, input):
    text = input.group(2)
    for char in text:
        if char in HTML_ENCODINGS:
            text = text.replace(char, HTML_ENCODINGS[char])
    bah = uri + text
    url = "https://tinyurl.com/api-create.php?url={0}".format(bah)
    a = web.get(url)
    a = a.replace("http:", "https:")
    code.reply(a)
latex.commands = ['tex']
latex.priority = 'high'

if __name__ == '__main__':
    print __doc__.strip()

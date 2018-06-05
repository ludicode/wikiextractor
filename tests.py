# coding: utf-8
# This test must pass both in Python 2 and 3.
from __future__ import unicode_literals

import sys
import os.path
import unittest

from WikiExtractor import (
    normalize_title, unescape, ucfirst, lcfirst, split_parts,
    fully_qualified_template_title, NextFile
)


class TestNormalizeTitle(unittest.TestCase):

    def test_known_namespace(self):
        self.assertEqual(normalize_title("Template:  Births"), "Template:Births")
        self.assertEqual(normalize_title(" template:  births_"), "Template:Births")

    def test_not_known_namespace(self):
        self.assertEqual(normalize_title("Category:  Births"), "Category: Births")
        self.assertEqual(normalize_title("_category:  births___"), "Category: Births")

    def test_no_namespace(self):
        self.assertEqual(normalize_title("python"), "Python")
        self.assertEqual(normalize_title("python 3"), "Python 3")
        self.assertEqual(normalize_title("python__3"), "Python 3")


class TestStringUtils(unittest.TestCase):

    def test_unescape(self):
        self.assertEqual(unescape('&#34;'), '"')
        self.assertEqual(unescape('&#38;'), '&')
        self.assertEqual(unescape('&#x3042;'), '\u3042')
        if sys.maxunicode > 0xFFFF:
            # Python 3 or UCS-4 build of Python 2
            self.assertEqual(unescape('&#x1D546;'), '\U0001D546')
            self.assertEqual(unescape('&#x1d4c1;'), '\U0001d4c1')
        else:
            # UCS-2 build of Python 2
            self.assertEqual(unescape('&#x1D546;'), '&#x1D546;')
            self.assertEqual(unescape('&#x1d4c1;'), '&#x1d4c1;')

    def test_ucfirst(self):
        self.assertEqual(ucfirst('python'), 'Python')

    def test_lcfirst(self):
        self.assertEqual(lcfirst('Python'), 'python')


class TestSplitParts(unittest.TestCase):

    def test_simple(self):
        self.assertEqual(split_parts("p=q|q=r|r=s"), ['p=q', 'q=r', 'r=s'])

    def test_complex(self):
        self.assertEqual(split_parts('{{#if: {{{1}}} | {{lc:{{{1}}} | "parameter missing"}}'),
                         ['{{#if: {{{1}}} ', ' {{lc:{{{1}}} ', ' "parameter missing"}}'])

        self.assertEqual(split_parts('''{{if:|
      |{{#if:the president|
           |{{#if:|
               [[Category:Hatnote templates|A{{PAGENAME}}]]
            }}
       }}
     }}'''), ['''{{if:|
      |{{#if:the president|
           |{{#if:|
               [[Category:Hatnote templates|A{{PAGENAME}}]]
            }}
       }}
     }}'''])


class TestFullyQualifiedTemplateTitle(unittest.TestCase):

    def test_main_namespace(self):
        self.assertEqual(fully_qualified_template_title(':Python'), 'Python')
        self.assertEqual(fully_qualified_template_title(':python'), 'Python')

    def test_other_namespace(self):
        self.assertEqual(fully_qualified_template_title('User:Orange'), 'User:Orange')


class TestNextFile(unittest.TestCase):

    def test_next(self):
        f = NextFile('out')
        self.assertEqual(next(f), 'out{}AA/wiki_00'.format(os.path.sep))
        self.assertEqual(next(f), 'out{}AA/wiki_01'.format(os.path.sep))
        for _ in range(97):
            next(f)
        self.assertEqual(next(f), 'out{}AA/wiki_99'.format(os.path.sep))
        self.assertEqual(next(f), 'out{}AB/wiki_00'.format(os.path.sep))


if __name__ == '__main__':
    unittest.main()

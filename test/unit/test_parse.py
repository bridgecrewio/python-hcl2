"""Test the parsing of lines and files"""
import time
from unittest import TestCase

import hcl2
from hcl2.parser import strip_line_comment


class TestParse(TestCase):
    """ Test parsing a variety of hcl files"""

    def test_strip_line_comment(self):
        """
        Test comment stripping from lines
        """
        test_strings = [
            ('x = "123"', 'x = "123"'),
            ('# a basic "comment', ''),
            ('x = "123" # an end of line "comment', 'x = "123" '),
            ('x = "12#3"', 'x = "12#3"'),
            ('x = "12#3" # comment', 'x = "12#3" '),
            ('x = "1#2#3" # comment', 'x = "1#2#3" '),
            ('x = "12#3" + "12#3" # comment', 'x = "12#3" + "12#3" '),
            ('# x = "12#3" + "12#3" # comment', ''),
            ('//# x = "12#3" + "12#3" # comment', ''),
            ('// a ba/*sic "comment', ''),
            ('x = "123" // an end of line "comment', 'x = "123" '),
            ('x = "12//3"', 'x = "12//3"'),
            ('x = "12//3" // comment', 'x = "12//3" '),
            ('//', ''),
            ('#', ''),
            ('a = "123" #', 'a = "123" '),
            ('   /*', '   '),
            ('a = "12/*" #commen" //t', 'a = "12/*" '),
            ('a = "12/* an actual unclosed string', 'a = "12/* an actual unclosed string'),

        ]

        for test_string, expected in test_strings:
            result, _, _ = strip_line_comment(test_string)
            self.assertEqual(result, expected)

    def test_parse_comments(self):
        """
        test different combinations of unclosed quotes in regular comments.
        Each of these should pass parsing the actual line stripping logic
        is tested above, so these can be basic
        """
        test_strings = [
            '# a basic "comment',
            'x = "123" # an end of line "comment',
        ]

        for test_string in test_strings:
            try:
                hcl2.loads(test_string)
            except Exception as err:
                self.fail(f'The parser threw an exception for the line: {test_string}, {err}')

        # now test multiline comment cases that should all pass parsing
        test_strings = [
            """resource "aws_s3_bucket" "b" {
    bucket = "123"
    /* this is the start of a multi line comment
    here is an "unclosed quote
    (well, it's closed here) " */
}""", """resource "aws_s3_bucket" "b" {
    bucket = "123"
    /* this is the start of a multi line comment
    here is an "unclosed quote
    (well, it's closed here) "
    */
}""", """resource "aws_s3_bucket" "b" {
    bucket = "123" /* this is the start of a multi line comment "with an unclosed quote
    (well, it's closed here) "
    */
}""", """resource "aws_s3_bucket" "b" {
    bucket = "123" # /* this is the start of a not actually multi line comment "with an unclosed quote
}""", """resource "aws_s3_bucket" "b" {
    bucket = "123" /* this is a one line comment "with an unclosed quote */
}""", """resource "aws_s3_bucket" "b" {
     /* this is a one line comment "with an unclosed quote */
     bucket = "123"
}""", """resource "aws_s3_bucket" "b" {
    /* this is the start of a multi line comment
    here is an "unclosed quote
    (well, it's closed here) " */
    bucket = "123"
}"""
        ]

        for test_string in test_strings:
            try:
                hcl2.loads(test_string)
            except ValueError as err:
                self.fail(f'The parser threw an exception for the string: {test_string}. {err}')

        # failure scenarios are handled in the other tests

    def test_parse_windows_line_separator(self):
        """Test parsing a windows line separator"""

        crlf_str = 'variable "region" {\r\n}\r\n'

        result = hcl2.loads(crlf_str)

        self.assertDictEqual(
            result,
            {
                "variable": [
                    {
                        "region": {
                            "__start_line__": 1,
                            "__end_line__": 2
                        }
                    }
                ]
            }
        )

    def test_parse_escaped_interpolation(self):
        """Escaped "$${" sequences are plain text and parse as literal strings"""
        cases = [
            ('"$${"', '$${'),
            ('"$${var.name}"', '$${var.name}'),
            ('"prefix-$${literal}-${var.name}"', 'prefix-$${literal}-${var.name}'),
            ('"$$${var.name}"', '$$${var.name}'),
            ('"$$"', '$$'),
            ('"100$"', '100$'),
        ]

        for literal, expected in cases:
            with self.subTest(literal=literal):
                result = hcl2.loads(f'v = {literal}\n')
                self.assertEqual(result['v'], [expected])

    def test_parse_escaped_interpolation_is_fast(self):
        """Parse time stays flat when an escaped "$${" is followed by many other strings"""
        lines = ['  a = strcontains(var.name, "$${")']
        lines += [f'  s{i} = "value-{i}"' for i in range(40)]
        text = 'locals {\n' + '\n'.join(lines) + '\n}\n'

        start = time.monotonic()
        result = hcl2.loads(text)
        elapsed = time.monotonic() - start

        self.assertEqual(result['locals'][0]['s39'], ['value-39'])
        self.assertLess(elapsed, 5)

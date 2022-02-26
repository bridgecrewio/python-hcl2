"""A parser for HCL2 implemented using the Lark parser"""
from importlib import resources
from pathlib import Path
from typing import Dict

from lark import Lark

from hcl2.transformer import DictTransformer

PARSER_FILE = Path(__file__).parent / ".lark_cache.bin"
LARK_GRAMMAR = resources.read_text(__package__, "hcl2.lark")


def strip_line_comment(line: str):
    """
    Finds the start of a comment in the line, if any, and returns the line
    up to the comment, the token that started the comment (#, //, or /*),
    and the line after the comment token
    """
    comment_tokens = ['#', '//', '/*']

    # manual iteration; trying to avoid a bunch of repeated "in" searches
    index = 0
    while index < len(line):
        for token in comment_tokens:
            if index > len(line) - len(token):
                continue
            if line[index:index + len(token)] == token and \
                    line[0:index].replace('\\"', '').count('"') % 2 == 0:
                # we are not in a string, so this marks the start of a comment
                return line[0:index], token, line[index + len(token):]
        index += 1
# abcd#
    return line, None, None


class Hcl2:
    """Wrapper class for Lark"""

    def parse(self, text: str) -> Dict:
        """Parses a HCL file and returns a dict"""

        lark_parser = Lark(grammar=LARK_GRAMMAR, parser="lalr", cache=str(PARSER_FILE))
        tree = lark_parser.parse(text)
        return DictTransformer().transform(tree)


hcl2 = Hcl2()

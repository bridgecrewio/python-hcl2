"""A Lark Transformer for transforming a Lark parse tree into a Python dict"""
from __future__ import annotations

import re
import sys
from typing import Any, TYPE_CHECKING

from lark import Transformer, Token
from lark.visitors import v_args

if TYPE_CHECKING:
    from lark.tree import Meta

HEREDOC_PATTERN = re.compile(r"<<([a-zA-Z][a-zA-Z0-9._-]+)\n(([^\n]|\n)*)\n\s*\1", re.S)
HEREDOC_TRIM_PATTERN = re.compile(r"<<-([a-zA-Z][a-zA-Z0-9._-]+)\n(([^\n]|\n)*)\n\s*\1", re.S)

START_LINE = "__start_line__"
END_LINE = "__end_line__"

NO_BLOCK_LABEL_TYPES = {"locals", "terraform"}
ONE_BLOCK_LABEL_TYPES = {"module", "provider", "variable"}
TWO_BLOCK_LABEL_TYPES = {"data", "resource"}


# pylint: disable=missing-docstring,unused-argument
class DictTransformer(Transformer[Token, "dict[str, list[dict[str, Any]]]"]):
    def float_lit(self, args: list) -> float:
        return float("".join([str(arg) for arg in args]))

    def int_lit(self, args: list) -> int:
        return int("".join([str(arg) for arg in args]))

    def expr_term(self, args: list) -> Any:
        args = self.strip_new_line_tokens(args)

        #
        if args[0] == "true":
            return True
        if args[0] == "false":
            return False
        if args[0] == "null":
            return None

        # if the expression starts with a paren then unwrap it
        if args[0] == "(":
            return args[1]
        # otherwise return the value itself
        return args[0]

    def index_expr_term(self, args: list[str]) -> str:
        args = self.strip_new_line_tokens(args)
        return f"{str(args[0])}{str(args[1])}"

    def index(self, args: list[int | str]) -> str:
        args = self.strip_new_line_tokens(args)
        return f"[{str(args[0])}]"

    def get_attr_expr_term(self, args: list[str]) -> str:
        return f"{str(args[0])}{str(args[1])}"

    def get_attr(self, args: list[str]) -> str:
        return f".{args[0]}"

    def attr_splat_expr_term(self, args: list[str]) -> str:
        return f"{args[0]}{args[1]}"

    def attr_splat(self, args: list[str]) -> str:
        return f".*{''.join(args)}"

    def full_splat_expr_term(self, args: list[str]) -> str:
        return f"{args[0]}{args[1]}"

    def full_splat(self, args: list[str]) -> str:
        return f"[*]{''.join(args)}"

    def tuple(self, args: list) -> list:
        return [self.to_string_dollar(arg) for arg in self.strip_new_line_tokens(args)]

    def object_elem(self, args: list) -> dict[str, Any]:
        # This returns a dict with a single key/value pair to make it easier to merge these
        # into a bigger dict that is returned by the "object" function
        key = self.strip_quotes(args[0])
        value = self.to_string_dollar(args[1])

        return {
            key: value,
        }

    def object(self, args: list) -> dict:
        args = self.strip_new_line_tokens(args)
        result: dict[str, Any] = {}
        for arg in args:
            result.update(arg)
        return result

    def function_call(self, args: list) -> str:
        args = self.strip_new_line_tokens(args)
        args_str = ""
        if len(args) > 1:
            args_str = ",".join([str(arg) for arg in args[1]])
        return f"{str(args[0])}({args_str})"

    def arguments(self, args: list) -> list:
        return args

    @v_args(meta=True)
    def block(self, meta: Meta, args: list) -> dict[str, Any]:
        args = self.strip_new_line_tokens(args)

        # if the last token is a string instead of an object then the block is empty
        # such as 'foo "bar" "baz" {}'
        # in that case append an empty object
        if isinstance(args[-1], str):
            args.append({})

        result: dict[str, Any] = {}
        current_level = result
        for arg in args[0:-2]:
            current_level[self.strip_quotes(arg)] = {}
            current_level = current_level[self.strip_quotes(arg)]

        current_level[self.strip_quotes(args[-2])] = args[-1]

        if args[0] in TWO_BLOCK_LABEL_TYPES and isinstance(args[1], str) and isinstance(args[2], str):
            label_1 = self.strip_quotes(args[1])
            label_2 = self.strip_quotes(args[2])
            result[args[0]][label_1][label_2][START_LINE] = meta.line
            result[args[0]][label_1][label_2][END_LINE] = meta.end_line

        if args[0] in ONE_BLOCK_LABEL_TYPES and isinstance(args[1], str):
            label_1 = self.strip_quotes(args[1])
            result[args[0]][label_1][START_LINE] = meta.line
            result[args[0]][label_1][END_LINE] = meta.end_line

        if args[0] in NO_BLOCK_LABEL_TYPES:
            result[args[0]][START_LINE] = meta.line
            result[args[0]][END_LINE] = meta.end_line

        return result

    def attribute(self, args: list) -> dict[str, Any]:
        key = str(args[0])
        if key.startswith('"') and key.endswith('"'):
            key = key[1:-1]
        value = self.to_string_dollar(args[1])

        return {
            key: value,
        }

    def conditional(self, args: list) -> str:
        args = self.strip_new_line_tokens(args)
        return f"{args[0]} ? {args[1]} : {args[2]}"

    def binary_op(self, args: list) -> str:
        return " ".join([str(arg) for arg in args])

    def unary_op(self, args: list) -> str:
        return "".join([str(arg) for arg in args])

    def binary_term(self, args: list) -> str:
        args = self.strip_new_line_tokens(args)
        return " ".join([str(arg) for arg in args])

    def body(self, args: list) -> dict[str, list]:
        # A body can have multiple attributes with the same name
        # For example multiple Statement attributes in a IAM resource body
        # So This returns a dict of attribute names to lists
        # The attribute values will always be lists even if they aren't repeated
        # and only contain a single entry
        args = self.strip_new_line_tokens(args)
        result: dict[str, Any] = {}
        for arg in args:
            for key, value in arg.items():
                key = str(key)
                if key not in result:
                    result[key] = [value]
                else:
                    if isinstance(result[key], list):
                        if isinstance(value, list):
                            result[key].extend(value)
                        else:
                            result[key].append(value)
                    else:
                        result[key] = [result[key], value]

        return result

    def start(self, args: list) -> dict[str, list[dict[str, Any]]]:
        args = self.strip_new_line_tokens(args)
        return args[0]

    def binary_operator(self, args: list) -> str:
        return str(args[0])

    def heredoc_template(self, args: list) -> str:
        match = HEREDOC_PATTERN.match(str(args[0]))
        if not match:
            raise RuntimeError(f"Invalid Heredoc token: {args[0]}")
        return f'"{match.group(2)}"'

    def heredoc_template_trim(self, args: list) -> str:
        # See https://github.com/hashicorp/hcl2/blob/master/hcl/hclsyntax/spec.md#template-expressions
        # This is a special version of heredocs that are declared with "<<-"
        # This will calculate the minimum number of leading spaces in each line of a heredoc
        # and then remove that number of spaces from each line
        match = HEREDOC_TRIM_PATTERN.match(str(args[0]))
        if not match:
            raise RuntimeError(f"Invalid Heredoc token: {args[0]}")

        text = match.group(2)
        lines = text.split("\n")

        # calculate the min number of leading spaces in each line
        min_spaces = sys.maxsize
        for line in lines:
            leading_spaces = len(line) - len(line.lstrip(" "))
            min_spaces = min(min_spaces, leading_spaces)

        # trim off that number of leading spaces from each line
        lines = [line[min_spaces:] for line in lines]

        return '"{}"'.format("\n".join(lines))

    def for_tuple_expr(self, args: list) -> str:
        args = self.strip_new_line_tokens(args)
        for_expr = " ".join([str(arg) for arg in args[1:-1]])
        return f"[{for_expr}]"

    def for_intro(self, args: list) -> str:
        args = self.strip_new_line_tokens(args)
        return " ".join([str(arg) for arg in args])

    def for_cond(self, args: list) -> str:
        args = self.strip_new_line_tokens(args)
        return " ".join([str(arg) for arg in args])

    def for_object_expr(self, args: list) -> str:
        args = self.strip_new_line_tokens(args)
        for_expr = " ".join([str(arg) for arg in args[1:-1]])
        return f"{{{for_expr}}}"

    def strip_new_line_tokens(self, args: list[Any]) -> list[Any]:
        """
        Remove new line and Discard tokens.
        The parser will sometimes include these in the tree so we need to strip them out here
        """
        return [arg for arg in args if arg != "\n"]

    def to_string_dollar(self, value: Any) -> Any:
        """Wrap a string in ${ and }"""
        if isinstance(value, str):
            if value.startswith('"') and value.endswith('"'):
                return str(value)[1:-1]
            return f"${{{value}}}"
        return value

    def strip_quotes(self, value: Any) -> Any:
        """Remove quote characters from the start and end of a string"""
        if isinstance(value, str):
            if value.startswith('"') and value.endswith('"'):
                return str(value)[1:-1]
        return value

    def identifier(self, value: Any) -> Any:
        # Making identifier a token by capitalizing it to IDENTIFIER
        # seems to return a token object instead of the str
        # So treat it like a regular rule
        # In this case we just convert the whole thing to a string
        return str(value[0])

import random
from secrets import token_hex

import jinja2
from jinja2 import nodes
from jinja2.ext import Extension


def token():
    """ Sample global function """
    return token_hex()


@jinja2.contextfilter
def shuffle(context, value: str):
    """ Sample filter """
    letters = list(value)
    random.shuffle(letters)
    return ''.join(letters)


def is_digit(value: str):
    """ Sample test function """
    return isinstance(value, int) or value.isdigit()


class ReverseExtension(Extension):
    tags = {'reverse'}

    def parse(self, parser):
        lineno = next(parser.stream).lineno
        body = parser.parse_statements(['name:endreverse'], drop_needle=True)
        return nodes.CallBlock(self.call_method('_reverse', []), [], [], body).set_lineno(lineno)

    async def _reverse(self, caller):
        rv = await caller()
        return nodes.Markup(str(rv)[::-1])

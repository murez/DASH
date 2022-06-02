# This file is used to parse input.run
# It can parse input args in input.run
# It will turn args into tags and render it to scheduler


# ------------------------------------------------------------------------------
# parse.py

# Example of using parse.py to parse the following grammar:

#     KEY-VALUE-PAIR: HASHTAG KEY EQUAL VALUE


# ------------------------------------------------------------------------------

import scheduler


KEYWORDS = ["TAG"]


def parseline(input_line: str) -> list() or None:
    """
    Parse a line of input
    """
    input_line = input_line.strip()
    index = 0
    while(index < len(input_line)):
        # Get the next token
        tok = input_line[index]
        if tok == '#':
            # Parse a comment
            input_line = input_line[index+1:]
            try:
                key = input_line.split('=')[0]
                value = input_line.split('=')[1]
            except:
                return None
            if key in KEYWORDS:
                return [key, value]
        else:
            return None


def parse(filename: str) -> bool:
    """
    Parse input.run
    """
    # Open and read input.run
    with open(filename, 'r') as f:
        for line in f.readlines():
            # Give the lexer some input
            tok = parseline(line)
            if tok is not None:
                print(tok)

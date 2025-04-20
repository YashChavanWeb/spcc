import re

# Define regex patterns for different token types
KEYWORDS = {"int", "float", "char", "if", "else", "return"}
KEYWORD_PATTERN = r"\b(?:" + "|".join(KEYWORDS) + r")\b"
IDENTIFIER_PATTERN = r"[a-zA-Z_][a-zA-Z0-9_]*"
CONSTANT_PATTERN = r"\b\d+\b"
OPERATOR_PATTERN = r"[+\-*/=]"
PUNCTUATION_PATTERN = r"[;,()]"

# Combine all patterns into one regex
TOKEN_PATTERN = (
    f"(?P<Keyword>{KEYWORD_PATTERN})|"
    f"(?P<Identifier>{IDENTIFIER_PATTERN})|"
    f"(?P<Constant>{CONSTANT_PATTERN})|"
    f"(?P<Operator>{OPERATOR_PATTERN})|"
    f"(?P<Punctuation>{PUNCTUATION_PATTERN})"
)


def lex_analyze(input_string):
    # List to store token details
    tokens = []

    # Find all matches in the input string
    for match in re.finditer(TOKEN_PATTERN, input_string):
        kind = match.lastgroup
        value = match.group(kind)

        if kind == "Keyword":
            tokens.append((value, "Keyword"))
        elif kind == "Identifier":
            tokens.append((value, "Identifier"))
        elif kind == "Constant":
            tokens.append((value, "Constant"))
        elif kind == "Operator":
            tokens.append((value, "Operator"))
        elif kind == "Punctuation":
            tokens.append((value, "Punctuation"))

    return tokens


# Example input
input_string = "int sum = a + 5;"

# Perform lexical analysis
tokens = lex_analyze(input_string)

# Print results
for token in tokens:
    print(f"{token[0]} : {token[1]}")

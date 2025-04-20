import re

# Function to convert infix expression to postfix notation
def infix_to_postfix(infix):
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, 'u-': 3}  # Unary minus has highest precedence
    stack = []
    postfix = []
    prev_token = None

    for token in infix:
        if token.isalnum():  # Operand (Variable)
            postfix.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while stack and stack[-1] != '(':
                postfix.append(stack.pop())
            stack.pop()  # Remove '('
        else:  # Operator
            # Handling unary minus
            if token == '-' and (prev_token is None or prev_token in "(-+*/"):
                token = 'u-'  # Mark as unary minus

            while stack and stack[-1] in precedence and precedence[token] <= precedence[stack[-1]]:
                postfix.append(stack.pop())

            stack.append(token)

        prev_token = token

    while stack:
        postfix.append(stack.pop())

    return postfix

# Function to generate Three Address Code (TAC)
def generate_tac(postfix):
    stack = []
    tac = []
    temp_count = 1

    for token in postfix:
        if token.isalnum():  # Operand
            stack.append(token)
        elif token == 'u-':  # Unary minus
            op = stack.pop()
            temp_var = f"t{temp_count}"
            tac.append(f"{temp_var} = - {op}")
            stack.append(temp_var)
            temp_count += 1
        else:  # Binary operator
            op2 = stack.pop()
            op1 = stack.pop()
            temp_var = f"t{temp_count}"
            tac.append(f"{temp_var} = {op1} {token} {op2}")
            stack.append(temp_var)
            temp_count += 1

    return tac

# Main function
def main():
    # Predefined input
    user_input = "a + b * (c - d) / e"

    # Remove spaces and split characters properly
    infix = re.findall(r'[a-zA-Z0-9]+|[\+\-\*/\(\)]', user_input)

    # Convert to postfix notation
    postfix = infix_to_postfix(infix)
    print(f"\nPostfix Notation: {''.join(postfix)}")

    # Generate Three Address Code
    tac = generate_tac(postfix)
    
    print("\nThree Address Code (TAC):")
    for line in tac:
        print(line)

if __name__ == "__main__":
    main()

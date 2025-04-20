def shift_reduce_parser(input_string):
    grammar = {"T+T": "T", "T-T": "T", "T*T": "T", "id": "T"}

    # Initialize stack and input
    stack = ["$"]
    input_string += "$"
    pointer = 0

    def try_reduce():
        # Try to reduce from largest possible handles
        for size in range(3, 0, -1):  # Try handles of length 3, 2, 1
            if len(stack) >= size + 1:  # +1 because of '$' at bottom
                handle = "".join(stack[-size:])
                if handle in grammar:
                    for _ in range(size):
                        stack.pop()
                    stack.append(grammar[handle])
                    return f"Reduce {handle} → {grammar[handle]}"
        return None

    # Print header
    print(f"{'Stack':<30} {'Input':<30} Action")
    print(f"{''.join(stack):<30} {input_string[pointer:]:<30} Initial State")

    while True:
        # Try reducing if possible
        reduction = try_reduce()
        if reduction:
            print(f"{''.join(stack):<30} {input_string[pointer:]:<30} {reduction}")
            continue

        # Check for accept condition
        if input_string[pointer] == "$" and stack == ["$", "T"]:
            print(f"{''.join(stack):<30} {input_string[pointer:]:<30} Accept")
            break

        # Shift next symbol
        if input_string[pointer : pointer + 2] == "id":
            stack.append("id")
            pointer += 2
            print(f"{''.join(stack):<30} {input_string[pointer:]:<30} Shift")
        else:
            stack.append(input_string[pointer])
            pointer += 1
            print(f"{''.join(stack):<30} {input_string[pointer:]:<30} Shift")


# Example usage
input_string = "id+id*id"
shift_reduce_parser(input_string)

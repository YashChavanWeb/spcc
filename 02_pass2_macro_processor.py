def replace_macros_in_intermediate_code(mnt, mdt, ala, intermediate_code):
    """Expand macros in the intermediate code using MNT, MDT, and ALA."""
    expanded_code = []

    for line in intermediate_code:
        stripped = line.strip()

        for entry in mnt:
            macro_name = entry["Macro Name"]
            if stripped.startswith(macro_name):
                # Extract actual arguments
                args_str = stripped[len(macro_name) :].strip()
                args = [arg.strip() for arg in args_str.split(",")] if args_str else []
                arg_map = {f"#{i + 1}": args[i] for i in range(len(args))}

                # Expand macro
                mdt_index = entry["MDT Index"]
                while mdt[mdt_index].strip() != "MEND":
                    macro_line = mdt[mdt_index]
                    for placeholder, value in arg_map.items():
                        macro_line = macro_line.replace(placeholder, value)
                    expanded_code.append(macro_line)
                    mdt_index += 1
                break
        else:
            expanded_code.append(line)

    return expanded_code


def print_all_outputs(input_code, modified_macro_def, expanded_code, ala):
    print("Original Input Code:")
    for line in input_code:
        print(line)

    print("\nMacro Definition After Replacement:")
    for line in modified_macro_def:
        print(line)

    print("\nExpanded Intermediate Code (Pass 2 Output):")
    for line in expanded_code:
        print(line)

    print("\nArgument List Array (ALA):")
    print(f"{'Macro Index':<15}{'Argument Name':<20}{'Value'}")
    for entry in ala:
        print(f"{entry['Index']:<15}{entry['Formal Parameter']:<20}{entry['Value']}")


# Sample Input
input_code = [
    "MACRO",
    "ABC &arg1, &arg2",
    "    A1, &arg1",
    "    A2, &arg2",
    "MEND",
    "START",
    "ABC data1, data2",
    "END",
]

mnt = [{"Index": 1, "Macro Name": "ABC", "MDT Index": 1}]
mdt = ["ABC &arg1, &arg2", "    A1, #1", "    A2, #2", "MEND"]
ala = [
    {"Index": 1, "Formal Parameter": "&arg1", "Value": "data1"},
    {"Index": 2, "Formal Parameter": "&arg2", "Value": "data2"},
]
intermediate_code = ["START", "ABC data1, data2", "END"]

# Run Pass 2
expanded_code = replace_macros_in_intermediate_code(mnt, mdt, ala, intermediate_code)

# Create Modified Macro Definition with actual arguments
modified_macro_def = [
    "MACRO",
    f"ABC {ala[0]['Value']}, {ala[1]['Value']}",
    f"    A1, {ala[0]['Value']}",
    f"    A2, {ala[1]['Value']}",
    "MEND",
]

# Print all outputs
print_all_outputs(input_code, modified_macro_def, expanded_code, ala)

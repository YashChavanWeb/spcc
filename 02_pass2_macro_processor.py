def replace_macros_in_intermediate_code(mnt, mdt, ala, intermediate_code):
    """Expand macros in the intermediate code using MNT, MDT, and ALA."""
    expanded_code = []

    # Create a dictionary for fast lookup of actual argument values from ALA
    ala_dict = {entry["Formal Parameter"]: entry["Value"] for entry in ala}

    for line in intermediate_code:
        stripped = line.strip()

        # Check if the line is a macro call (starts with a macro name)
        for entry in mnt:
            if stripped.startswith(entry["Macro Name"]):
                macro_name = entry["Macro Name"]
                mdt_index = entry["MDT Index"] - 1  # MDT is 0-based index
                mdt_entry = mdt[mdt_index]

                # Extract arguments from the macro call (e.g., "ABC data1, data2" -> ["data1", "data2"])
                args = (
                    stripped[len(macro_name) :].strip()[1:-1].split(",")
                    if stripped[len(macro_name) :].strip()
                    else []
                )
                args = [arg.strip() for arg in args]

                # Replace formal parameters in MDT entry with actual argument values from ALA
                for i, param in enumerate(args):
                    formal_param = f"&arg{i + 1}"  # e.g., &arg1, &arg2
                    if formal_param in ala_dict:
                        mdt_entry = mdt_entry.replace(
                            formal_param, ala_dict[formal_param]
                        )

                # Add the expanded macro code to the result
                expanded_code.append(mdt_entry)
                break
        else:
            # If no macro match, just add the line as is
            expanded_code.append(line)

    return expanded_code


def print_expanded_code(expanded_code):
    """Print the expanded intermediate code."""
    print("\nExpanded Intermediate Code (Pass 2 Output):")
    for line in expanded_code:
        print(line)


def print_ala_table(ala):
    """Print the Argument List Array (ALA) table."""
    print("\nArgument List Array (ALA):")
    print(f"{'Macro Index':<15}{'Argument Name':<20}{'Value'}")
    for entry in ala:
        print(f"{entry['Index']:<15}{entry['Formal Parameter']:<20}{entry['Value']}")


# Sample Input from Pass 1 Output
mnt = [{"Index": 1, "Macro Name": "ABC", "MDT Index": 1}]
mdt = ["ABC &arg1, &arg2", "    A1, #1", "    A2, #2", "MEND"]
ala = [
    {"Index": 1, "Formal Parameter": "&arg1", "Value": "data1"},
    {"Index": 2, "Formal Parameter": "&arg2", "Value": "data2"},
]
intermediate_code = ["START", "ABC data1, data2", "END"]

# Run Pass 2
expanded_code = replace_macros_in_intermediate_code(mnt, mdt, ala, intermediate_code)

# Display Expanded Code
print_expanded_code(expanded_code)

# Display ALA Table
print_ala_table(ala)

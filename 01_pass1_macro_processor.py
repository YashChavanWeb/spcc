def parse_macro_prototype(line):
    """Parse the macro prototype line and extract macro name and arguments."""
    parts = line.split(None, 1)
    macro_name = parts[0]
    arguments = []
    if len(parts) > 1:
        arguments = [arg.strip() for arg in parts[1].split(",")]
    return macro_name, arguments


def create_mnt_entry(mnt, macro_name, mdt_index):
    """Add an entry to the Macro Name Table (MNT)."""
    mnt.append(
        {"Index": len(mnt) + 1, "Macro Name": macro_name, "MDT Index": mdt_index}
    )


def create_ala_entries(ala, arguments):
    """Create Argument List Array (ALA) entries for the macro arguments."""
    return [
        {"Index": i + 1, "Formal Parameter": arg} for i, arg in enumerate(arguments)
    ]


def replace_formal_args(line, ala):
    """Replace formal parameters with actual argument indices."""
    for entry in ala:
        line = line.replace(entry["Formal Parameter"], f"#{entry['Index']}")
    return line


def macro_pass1(assembly_code_lines):
    mnt = []
    mdt = []
    ala = []
    intermediate_code = []
    inside_macro = False
    mdt_index = 1
    macro_name = ""
    current_ala = []

    for line in assembly_code_lines:
        stripped = line.strip()

        if stripped == "MACRO":
            inside_macro = True
            continue

        if inside_macro:
            if not macro_name:  # First line after MACRO is the macro prototype
                macro_name, arguments = parse_macro_prototype(stripped)
                create_mnt_entry(mnt, macro_name, mdt_index)

                # Create ALA and add it
                current_ala = create_ala_entries(ala, arguments)
                ala.extend(current_ala)

                # Add the macro prototype to the MDT
                mdt.append(f"{macro_name} {', '.join(arguments)}")
                mdt_index += 1
                continue

            if stripped == "MEND":
                mdt.append("MEND")
                inside_macro = False
                mdt_index += 1
                macro_name = ""
                current_ala = []
                continue

            # Replace formal parameters with actual arguments
            mdt.append(replace_formal_args(stripped, current_ala))
            mdt_index += 1
        else:
            intermediate_code.append(line)

    return mnt, mdt, ala, intermediate_code


def print_table(title, headers, rows):
    """Helper function to print tables in a formatted way."""
    print(f"\n{title}")
    if not rows:
        print("(No entries)")
        return

    col_widths = [
        max(len(str(row[h])) for row in rows + [dict(zip(headers, headers))]) + 2
        for h in headers
    ]
    header_row = (
        "| " + " | ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers)) + " |"
    )
    separator = "|" + "|".join("-" * (w + 2) for w in col_widths) + "|"
    print(header_row)
    print(separator)

    for row in rows:
        row_str = (
            "| "
            + " | ".join(
                str(row[h]).ljust(col_widths[i]) for i, h in enumerate(headers)
            )
            + " |"
        )
        print(row_str)


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

# Run Pass 1
mnt, mdt, ala, intermediate_code = macro_pass1(input_code)

# Display Tables and Intermediate Code
print_table("Macro Name Table (MNT)", ["Index", "Macro Name", "MDT Index"], mnt)
print_table(
    "Macro Definition Table (MDT)",
    ["Index", "MDT Entry"],
    [{"Index": i + 1, "MDT Entry": entry} for i, entry in enumerate(mdt)],
)
print_table("Argument List Array (ALA)", ["Index", "Formal Parameter"], ala)

print("\nIntermediate Code (Output of Pass 1):")
for line in intermediate_code:
    print(line)

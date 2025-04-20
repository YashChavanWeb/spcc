import re


def simple_optimize_cpp(code: str) -> str:
    lines = code.strip().split("\n")
    output = []
    constants = {}

    for line in lines:
        original_line = line
        stripped = line.strip()

        # Skip empty lines or lines without content
        if not stripped:
            output.append(line)
            continue

        # Detect and store constant integer assignments
        const_match = re.match(r"int\s+(\w+)\s*=\s*(\d+);", stripped)
        if const_match:
            var, val = const_match.groups()
            constants[var] = val
            output.append(line)
            continue

        # Replace known constants in the line
        for var, val in constants.items():
            line = re.sub(rf"\b{var}\b", val, line)

        # Optimization: x * 2 => x + x
        line = re.sub(r"(\b\w+\b)\s*\*\s*2", r"\1 + \1", line)

        # Optimization: x + 0 or 0 + x => x
        line = re.sub(r"\b(\w+)\s*\+\s*0\b", r"\1", line)
        line = re.sub(r"\b0\s*\+\s*(\w+)\b", r"\1", line)

        # Optimization: constant math (e.g., 10 / 2)
        def eval_math(match):
            try:
                return str(eval(match.group(0)))
            except:
                return match.group(0)

        line = re.sub(r"\b\d+\s*[\+\-\*/]\s*\d+\b", eval_math, line)

        # Optimization: while(i < something - const) => temp var
        if "while" in line and re.search(r"<\s*\w+\s*-\s*\d+", line):
            cond_match = re.search(r"(\w+)\s*<\s*(\w+)\s*-\s*(\d+)", line)
            if cond_match:
                left, right, num = cond_match.groups()
                new_var = "temp_limit"
                assign_line = f"    int {new_var} = {right} - {num};"
                line = re.sub(rf"{right}\s*-\s*{num}", new_var, line)
                output.append(assign_line)
                output.append(line)
                continue

        output.append(line)

    return "\n".join(output)


# Example usage:

input_code = """
int a = 10;
int b = 20;
int c = a * 2 + 0;
int d = b - 5;
while (i < d - 3) {
    // some loop logic
}
"""

optimized_code = simple_optimize_cpp(input_code)
print(optimized_code)

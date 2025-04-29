variables = {}

def interpret_block(lines, start_index):
    i = start_index
    while i < len(lines):
        line = lines[i].strip()
        if line == "}":
            return i  # Ende des Blocks
        interpret(line)
        i += 1
    return i

def interpret(line):
    line = line.strip()


    #Variable setzen
    if line.startswith("set "):
        parts = line[4:-1].split(" = ")
        VarName = parts[0].strip()
        VarValue = eval(parts[1].strip(), {}, variables)
        variables[VarName] = VarValue

    elif line.startswith("write (") and line.endswith(")\\"):
        content = line[7:-2].strip()
        #löscht write ( )\
        if content.startswith("*") and content.endswith("*"):
            #löscht **
            print(content[1:-1])
        elif content in variables:
            print(variables[content])
        else:
            print(f"Error: '{content}' not defined")

    # if-Anweisung (incase)
    elif line.startswith("incase "):
        condition = line[7:].strip()
        if condition.endswith("{"):
            condition = condition[:-1].strip()
            try:
                if eval(condition, {}, variables):
                    return "start_block"  # Signalisiere, dass Block folgt
                else:
                    return "skip_block"
            except Exception as e:
                print(f"Condition Error: {e}")
                return "skip_block"

with open("my_program.mini", "r") as file:
    lines = file.readlines()

i = 0
while i < len(lines):
    result = interpret(lines[i])
    if result == "start_block":
        i += 1
        i = interpret_block(lines, i)
    elif result == "skip_block":
        # Block überspringen
        i += 1
        while i < len(lines) and lines[i].strip() != "}":
            i += 1
    i += 1
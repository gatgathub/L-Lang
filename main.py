import sys


def fwrite(file_n, cont):
    file = open(file_n, "w")
    file.write(str(cont))
    file.close()


def parse(text, delim=" "):
    str(text)
    text += delim
    new = []
    tempstr = ""
    for x in text:
        if x == delim:
            new.append(tempstr)
            tempstr = ""
        else:
            tempstr += x
    return new


def parse_n(text):
    str(text)
    new = ""
    for x in text:
        if x == "\\":
            break
        else:
            new += x
    return new


def fwrite(file_n, cont):
    file = open(file_n, "w")
    file.write(str(cont))
    file.close()


def fappend(file_n, cont):
    file = open(file_n, "a")
    file.write(str(cont))
    file.close()


def ftouch(file_n, mode, cont):
    file = open(file_n, mode)
    if mode == "w" or mode == "a":
        file.write(str(cont))
        file.close()
    else:
        if file_exists(file_n):
            read = file.read()
            file.close()
            return read
        else: return False


def file_exists(file_n):
    try:
        file = open(file_n, "r")
    except Exception:
        return False
    else:
        file.close()
        return True
    

def fread(file_n):
    if file_exists(file_n):
        file = open(file_n, "r")
        read = file.read()
        file.close()
        return read
    else: return False


def freadlines(file_n):
    if file_exists(file_n):
        file = open(file_n, "r")
        read = file.readlines()
        file.close()
        return read
    else: return False


vars = {}
if len(sys.argv) < 2:
    program = input("Program: (auto fills the .l) ") + ".l"
    prog_f = program
else:
    program = sys.argv[1]
    prog_f = program
new_f = program + ".py"
print_b = ""
if file_exists(prog_f):
    fwrite(new_f, "")
    lines = freadlines(prog_f)
    i = 0
    #for x in lines:
    #    lines[i] = parse_n(x)
    #    i += 1
    
    # mode 0 = function
    # mode 1 = var
    cnt = 0
    for e in lines:
        i = 0
        string = ""
        chars = []
        mode = 0
        for x in lines[cnt]:
            chars.append(x)
        for x in lines[cnt]:
            if i == 0 and x == "$":
                mode = 1
                i += 1
                continue
            if mode == 0:
                if x == "(":
                    break
                else:
                    string += x
            else:
                if x == "=" or x == " ":
                    break
                else:
                    string += x
            i += 1
        if mode == 0 and string == "printf":
            if chars[7] == '"' or chars[7] == "'":
                start = 0
                for x in range(8):
                    del chars[0]
                string = ""
                for x in chars:
                    if x == '"' or x == "'":
                        break
                    else:
                        string += x
                print_b += string
            elif chars[7] == "$":
                start = 0
                for x in range(8):
                    del chars[0]
                string = ""
                for x in chars:
                    if x == " " or x == ")":
                        break
                    else:
                        string += x
                print_b += "{" + string + "}"
            elif chars[7] == ")":
                pass
            else:
                start = 0
                for x in range(7):
                    del chars[0]
                string = ""
                for x in chars:
                    if x == "r" or x == ")":
                        break
                    else:
                        string += x
                print_b += string
        elif mode == 0 and string == "input":
            if chars[6] == '"' or chars[6] == "'":
                start = 0
                for x in range(7):
                    del chars[0]
                string = ""
                for x in chars:
                    if x == '"' or x == "'":
                        break
                    else:
                        string += x
                print_b += string
                vars["_input"] = string
                fappend(new_f, f"_input = input(f\"{print_b}\")\n")
                print_b = ""
            elif chars[6] == "$":
                start = 0
                for x in range(7):
                    del chars[0]
                string = ""
                for x in chars:
                    if x == " " or x == ")":
                        break
                    else:
                        string += x
                print_b += "{" + string + "}"
                vars["_input"] = vars[string]
                fappend(new_f, f"_input = input(f\"{print_b}\")\n")
                print_b = ""
            elif chars[6] == ")":
                fappend(new_f, f"input(f\"{print_b}\")\n")
                print_b = ""
                pass
            else:
                start = 0
                for x in range(7):
                    del chars[0]
                string = ""
                for x in chars:
                    if x == " " or x == ")":
                        break
                    else:
                        string += x
                print_b += string
        #
        elif mode == 1:
            varname = string
            string = ""
            var_space = 0
            for x in range(len(varname)+1):
                del chars[0]
            spaces = 0
            for x in chars:
                if not(x == " " or x == "="):
                    break
                else:
                    spaces += 1
            for x in range(spaces):
                del chars[0]
            if chars[0] == "$":
                del chars[0]
                for x in chars:
                    if x == "\n": break
                    string += x
                if varname == "_printbuff":
                    print_b = string
                else:
                    vars[varname] = vars[string]
                fappend(new_f, f"{varname} = {string}\n")
            elif chars[0] == '"' or chars[0] == "'":
                del chars[0]
                del chars[len(chars) - 1]
                del chars[len(chars) - 1]
                for x in chars:
                    string += x
                vars[varname] = string
                fappend(new_f, f"{varname} = \"{string}\"\n")
            else:
                for x in chars:
                    string += x
                vars[varname] = int(string)
                fappend(new_f, f"{varname} = {string}\n")
        cnt += 1
fappend(new_f, f"print(f\"{print_b}\")")
print("Finished Compiling")
if len(sys.argv) < 2: input()

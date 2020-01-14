import re


# Function by Victor Neznanov
def ini_parse(filename: str):
    with open(filename, mode="r", encoding="utf-8") as f:
        lines = f.readlines()
        ini = {}

        section = "Default"
        for line in lines:
            search = re.search(r"\[(.+)\]", line)
            if search is not None:
                section = search.group(1)

            if line != "":
                search = re.search(r"(.+?)=(.*)", line)
                if search is not None:
                    if section in ini.keys():
                        ini[section].append((search.group(1), search.group(2)))
                    else:
                        ini[section] = [(search.group(1), search.group(2))]
        return ini

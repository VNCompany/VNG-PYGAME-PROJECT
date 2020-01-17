import re


# Class by Victor Neznanov
class INI:
    def __init__(self, lines: list):
        self.data = {}

        section = "Default"
        for line in lines:
            if line != "":
                search = re.search(r"\[(.+)\]", line)
                if search is not None:
                    clear_line = str(line).strip().replace("\n", "")
                    if (len(clear_line) > 2 and
                            clear_line[0] == "[" and
                            clear_line[-1] == "]"):
                        section = search.group(1)

                search = re.search(r"(.+?)=(.*)", line)
                if search is not None:
                    search_2 = re.search(r"\[(.+)\]", search.group(2))
                    value = search.group(2)
                    if search_2 is not None:
                        value = search_2.group(1).split(";")

                    if section in self.data.keys():
                        self.data[section].append((search.group(1), value))
                    else:
                        self.data[section] = [(search.group(1), value)]

    @staticmethod
    def ini_parse(filename: str):
        with open(filename, mode="r", encoding="utf-8") as f:
            lines = f.readlines()
            try:
                return INI(lines)
            except Exception as e:
                print("Load file error:", str(e))

    @staticmethod
    def ini_parse_text(text: str):
        return INI(text.split("\n"))

    def get(self, section, item: str):
        if section in self.data.keys():
            for key, value in self.data[section]:
                if key == item:
                    return value
        return None

    def section_exists(self, section: str):
        return section in self.data.keys()

    def get_sections(self):
        return list(self.data.keys())

    def item_exists(self, section: str, item: str):
        return self.get(section, item)

    def set(self, section: str, item: str, value):
        if type(value) is list:
            value = "[" + ";".join(value) + "]"
        elif type(value) is bool:
            value = "1" if bool(value) else "0"
        else:
            value = str(value)

        if self.item_exists(section, item):
            for i in range(len(self.data[section])):
                if self.data[section][i][0] == item:
                    self.data[section][i] = (self.data[section][i][0], value)
        elif self.section_exists(section):
            self.data[section].append((item, value))
        else:
            self.data[section] = [(item, value)]

    def save(self, filename):
        with open(filename, mode="w", encoding="utf-8") as f:
            for section in self.data.keys():
                f.write("[" + section + "]" + "\n")
                for item, value in self.data[section]:
                    f.write(item + "=" + value + "\n")

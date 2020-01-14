import re


# Class by Victor Neznanov
class INI:
    def __init__(self, lines: list):
        self.data = {}

        section = "Default"
        for line in lines:
            search = re.search(r"\[(.+)\]", line)
            if search is not None:
                section = search.group(1)

            if line != "":
                search = re.search(r"(.+?)=(.*)", line)
                if search is not None:
                    if section in self.data.keys():
                        self.data[section].append((search.group(1), search.group(2)))
                    else:
                        self.data[section] = [(search.group(1), search.group(2))]

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
        INI(text.split("\n"))

    def get(self, section: str, item: str):
        if section in self.data.keys():
            for key, value in self.data[section]:
                if key == item:
                    return value
        return None

    def section_exists(self, section: str):
        return section in self.data.keys()

    def get_sections(self):
        return list(self.data.keys())

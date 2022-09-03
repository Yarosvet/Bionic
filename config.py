import configparser
from os.path import exists


class Config:
    def __init__(self, path="config.ini"):
        self.path = path
        self.config = configparser.ConfigParser()
        default = {"rels": "https://raw.githubusercontent.com/Yarosvet/Bionic_books/master/rels.json"}
        if exists(path):
            self.config.read(self.path)
        else:
            self.config["DEFAULT"] = default
            with open(self.path, 'w') as f:
                self.config.write(f)

    def __setitem__(self, key, value):
        self.config["DEFAULT"][key] = value

    def __getitem__(self, item):
        return self.config["DEFAULT"][item]

    def save(self):
        with open(self.path, 'w') as f:
            self.config.write(f)

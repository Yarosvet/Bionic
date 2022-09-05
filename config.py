import configparser
from os.path import exists

default_config = {"rels": "https://raw.githubusercontent.com/Yarosvet/Bionic_books/master/rels.json",
                  "dark_mode": "0"}


class Config:
    def __init__(self, path="config.ini"):
        self.path = path
        self.config = configparser.ConfigParser()
        if exists(path):
            self.config.read(self.path)
        else:
            self.config["DEFAULT"] = default_config
            with open(self.path, 'w') as f:
                self.config.write(f)

    def __setitem__(self, key, value):
        self.config["DEFAULT"][key] = value

    def __getitem__(self, item):
        return self.config["DEFAULT"][item]

    def save(self):
        with open(self.path, 'w') as f:
            self.config.write(f)

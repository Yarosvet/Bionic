import json
from tarfile import TarFile
import os
from shutil import rmtree


def install_book(tar_path, book_id=None):
    if not os.path.exists("books/"):
        os.mkdir("books/")
    if book_id is None:
        with TarFile.open(name=tar_path, mode="r") as tf:
            tf.extract("book.json", "temp/")
        with open("temp/book.json", 'r') as f:
            book_id = json.load(f)["id"]
        os.remove("temp/book.json")
    book_path = f"books/book_{book_id}/"
    if os.path.exists(book_path):
        rmtree(book_path)
    os.mkdir(book_path)
    with TarFile.open(name=tar_path, mode="r") as tf:
        tf.extractall(path=book_path)


def check_by_filter(text, filter_expression="") -> bool:
    if filter_expression == "":
        return True
    for el in filter_expression.split():
        if el not in text:
            return False
    return True

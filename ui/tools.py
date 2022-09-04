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


def find_point_by_id(entry_points, p_id: int):
    for el in entry_points:
        if el["id"] == p_id:
            return el
        if el["nested"]:
            res = find_point_by_id(el["nested"], p_id=p_id)
            if res is not None:
                return res
    return None


def find_stage_by_id(stages, s_id: int):
    for el in stages:
        if el["id"] == s_id:
            return el
    return None


def check_by_filter(text, filter_expression="") -> bool:
    if filter_expression == "":
        return True
    for el in filter_expression.split():
        if el not in text:
            return False
    return True

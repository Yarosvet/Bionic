import json
import os
from dataclasses import dataclass


@dataclass
class Ending:
    book: "Book"
    id: int
    document: str


@dataclass
class Stage:
    book: "Book"
    id: int
    thesis: "Thesis"
    antithesis: "Thesis"


@dataclass
class Thesis:
    document: str
    target_type: str
    target_id: int
    book: "Book"

    @property
    def target(self) -> Stage | Ending:
        if self.target_type == "stage":
            return self.book.get_stage(self.target_id)
        return self.book.get_ending(self.target_id)


@dataclass
class EntryPoint:
    book: "Book"
    id: int
    name: str
    caption: str
    stage_id: int
    nested: list["EntryPoint"]

    def stage(self):
        return self.book.get_stage(self.stage_id)


class Book:
    def __init__(self, path: str):
        self.path = path
        with open(os.path.join(self.path, "book.json"), 'r') as fb:
            json_book = json.load(fb)
            self.id = json_book['id']
            self.name = json_book['name']
            self.cover = os.path.abspath(os.path.join(path, json_book['cover']))
            self.translation_date = json_book['translation_date']
            with open(os.path.join(self.path, json_book['stages']), 'r') as fs:
                self.stages_map = {el['id']: el for el in json.load(fs)}
            with open(os.path.join(self.path, json_book['endings']), 'r') as fe:
                self.endings = {el['id']: el for el in json.load(fe)}
            self.stage_documents = os.path.join(self.path, json_book['stage_documents'])
            self.ending_documents = os.path.join(self.path, json_book['ending_documents'])
            self.entry_points = self._update_entry_points(json_book['entry_points'])

    def get_stage(self, stage_id: int) -> Stage:
        s = self.stages_map[stage_id]
        with open(os.path.join(self.stage_documents, s['thesis']['document']), 'r') as f:
            t_doc = f.read()
        with open(os.path.join(self.stage_documents, s['antithesis']['document']), 'r') as f:
            at_doc = f.read()
        thesis = Thesis(t_doc, target_type=s['thesis']['target']['type'], target_id=s['thesis']['target']['id'],
                        book=self)
        antithesis = Thesis(at_doc, target_type=s['antithesis']['target']['type'],
                            target_id=s['antithesis']['target']['id'], book=self)
        return Stage(book=self, id=s['id'], thesis=thesis, antithesis=antithesis)

    def get_ending(self, ending_id: int) -> Ending:
        s = self.endings[ending_id]
        with open(os.path.join(self.ending_documents, s['document']), 'r') as f:
            doc = f.read()
        return Ending(book=self, id=s['id'], document=doc)

    def _update_entry_points(self, points: list) -> list[EntryPoint]:
        res = []
        for ep in points:
            res.append(EntryPoint(self, ep['id'], ep['name'], ep['caption'], ep['stage_id'],
                                  self._update_entry_points(ep['nested'])))
        return res

    def get_entry_point(self, point_id: int) -> EntryPoint:
        def recursive_search_point(p_id: int, points: list):
            res = None
            for el in points:
                if el.id == p_id:
                    return el
                res = recursive_search_point(p_id, el.nested)
                if res is not None:
                    break
            return res

        return recursive_search_point(point_id, self.entry_points)


class StagesStack:
    def __init__(self):
        self.back_stack = []

    def move_back(self):
        if self.can_move_back():
            self.back_stack.pop(-1)

    def current_stage(self) -> Stage | Ending:
        return self.back_stack[-1][0]

    def thesis_selected(self) -> bool:
        return self.back_stack[-1][1]

    def can_move_back(self) -> bool:
        return len(self.back_stack) >= 2

    def set_current_thesis(self, thesis_selected: bool):
        self.back_stack[-1][1] = thesis_selected

    def add_stage(self, stage: Stage):
        self.back_stack.append([stage, True])

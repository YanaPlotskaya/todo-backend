import json
import os
from typing import List


def print_with_indent(value, indent=0):
    number_of_tabs = '\t' * indent
    print(f"{number_of_tabs}{value}")


class Entry:
    def __init__(self, title, entries=None, parent=None):
        if entries is None:
            entries = []
        self.title = title
        self.entries = entries
        self.parent = parent

    def __str__(self):
        return self.title

    def add_entry(self, entry):
        entry.parent = self
        self.entries.append(entry)

    def print_entries(self, indent=0):
        print_with_indent(self, indent)
        for item in self.entries:
            item.print_entries(indent + 1)

    def entries_to_str(self):
        parse_entries = []
        for item in self.entries:
            parse_entries.append(item.json())
        return parse_entries

    def json(self):
        return {
            "title": self.title,
            "entries": self.entries_to_str()
        }

    @classmethod
    def from_json(cls, value):
        root_entry = Entry(value["title"])

        for entry in value.get("entries", []):
            child_entry = cls.from_json(entry)
            root_entry.add_entry(child_entry)

        return root_entry

    def save(self, path):
        with open(os.path.join(path, f'{self.title}.json'), 'w') as f:
            json.dump(self.json(), f)

    @classmethod
    def load(cls, filename):
        with open(filename, 'r') as f:
            entry_json = json.load(f)
        return cls.from_json(entry_json)


class EntryManager:
    def __init__(self, data_path):
        self.data_path = data_path
        self.entries: List[Entry] = []

    def save(self):
        for entry in self.entries:
            entry.save(self.data_path)

    def load(self):
        for filename in os.listdir(self.data_path):
            if filename.endswith(".json"):
                entry = Entry.load(os.path.join(self.data_path, filename))
                self.entries.append(entry)
        return self

    def add_entry(self, title: str):
        new_entry = Entry(title)
        self.entries.append(new_entry)

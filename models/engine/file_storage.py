#!/usr/bin/python3
"""serializes instances to JSON file, deserializes JSON file to instances"""

import json
from ast import literal_eval


class FileStorage:
    """file storage creation"""
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """returns the dictionary of objects"""
        return self.__objects

    def new(self, obj):
        """adds new object to __objects"""
        if obj:
            key = f"{type(obj).__name__}.{obj.id}"
            self.__objects[key] = obj

    def save(self):
        """saves objects to json file"""
        json_data = {}
        for key, value in self.__objects.items():
            json_data[key] = value.to_dict()
        with open(self.__file_path, 'w', encoding='utf-8') as fptr:
            json.dump(json_data, fptr)

    def reload(self):
        """reloads"""
        try:
            with open(self.__file_path, 'r', encoding='utf-8') as fptr:
                data = json.load(fptr)
                for key, obj in data.items():
                    new_obj = literal_eval(obj['__class__'])(**obj)
                    self.__objects[key] = new_obj
        except FileNotFoundError:
            pass

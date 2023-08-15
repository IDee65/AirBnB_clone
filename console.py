#!/usr/bin/python3
"""entry point of the command interpreter"""
import cmd
import shlex
from shlex import split
from ast import literal_eval
from models import storage


class HBNBCommand(cmd.Cmd):
    """HBNBCommand class

    Args:
        cmd (CMD): Command line interpreter
    """
    prompt = '(hbnb) '
    classes = {"BaseModel",
               "User", "State", "City", "Amenity", "Place", "Review"}

    def do_quit(self, _):
        "Quit command to exit the program"
        return True

    do_EOF = do_quit

    def do_create(self, line):
        """creates an object"""
        if len(line) == 0:
            print("** class name missing **")
            return
        if line not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        new_object = literal_eval(line)()
        print(new_object.id)
        new_object.save()

    def do_show(self, line):
        """shows an object"""
        if len(line) == 0:
            print("** class name missing **")
            return
        strings = split(line)
        if strings[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        if len(strings) == 1:
            print("** instance id missing **")
            return
        key_value = strings[0] + '.' + strings[1]
        if key_value not in storage.all():
            print("** no instance found **")
        else:
            print(storage.all()[key_value])

    def do_destroy(self, line):
        """deletes an object"""
        if len(line) == 0:
            print("** class name missing **")
            return
        strings = split(line)
        if strings[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        if len(strings) == 1:
            print("** instance id missing **")
            return
        key_value = strings[0] + '.' + strings[1]
        if key_value not in storage.all():
            print("** no instance found **")
            return
        del storage.all()[key_value]
        storage.save()

    def do_all(self, line):
        """prints all"""
        if len(line) == 0:
            print(list(obj for obj in storage.all().values()))
            return
        strings = split(line)
        if strings[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        print([obj for obj in storage.all().values()
               if strings[0] == type(obj).__name__])

    def do_update(self, line):
        """updates an object"""
        if len(line) == 0:
            print("** class name missing **")
            return
        strings = split(line)
        for string in strings:
            if string.startswith('"') and string.endswith('"'):
                string = string[1:-1]
        if strings[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        if len(strings) == 1:
            print("** instance id missing **")
            return
        key_value = strings[0] + '.' + strings[1]
        if key_value not in storage.all():
            print("** no instance found **")
            return
        if len(strings) == 2:
            print("** attribute name missing **")
            return
        if len(strings) == 3:
            print("** value missing **")
            return
        try:
            setattr(storage.all()[key_value],
                    strings[2], literal_eval(strings[3]))
        except Exception:  # pylint: disable=broad-except
            setattr(storage.all()[key_value], strings[2], strings[3])

    def emptyline(self):
        """passes"""

    def stripper(self, st):  # pylint: disable=invalid-name
        """strips that line"""
        newstring = st[st.find("(")+1:st.rfind(")")]
        newstring = shlex.shlex(newstring, posix=True)
        newstring.whitespace += ','
        newstring.whitespace_split = True
        return list(newstring)

    def dict_strip(self, st):  # pylint: disable=invalid-name
        """tries to find a dict while stripping"""
        newstring = st[st.find("(")+1:st.rfind(")")]
        try:
            newdict = newstring[newstring.find("{")+1:newstring.rfind("}")]
            return literal_eval("{" + newdict + "}")
        except Exception:  # pylint: disable=broad-except
            return None

    def default(self, line):
        """defaults"""
        sub_args = self.stripper(line)
        strings = list(shlex.shlex(line, posix=True))
        if strings[0] not in HBNBCommand.classes:
            print(f"*** Unknown syntax: {line}")
            return
        if strings[2] == "all":
            self.do_all(strings[0])
        elif strings[2] == "count":
            count = 0
            for obj in storage.all().values():
                if strings[0] == type(obj).__name__:
                    count += 1
            print(count)
            return
        elif strings[2] == "show":
            key = strings[0] + " " + sub_args[0]
            self.do_show(key)
        elif strings[2] == "destroy":
            key = strings[0] + " " + sub_args[0]
            self.do_destroy(key)
        elif strings[2] == "update":
            newdict = self.dict_strip(line)
            if type(newdict) is dict:  # pylint: disable=unidiomatic-typecheck
                for key, _ in newdict.items():
                    key_val = strings[0] + " " + sub_args[0]
                    self.do_update(key_val + ' f"{key}" "{val}"')
            else:
                key = strings[0]
                for _ in sub_args:
                    key = key + " " + 'f"{arg}"'
                self.do_update(key)
        else:
            print(f"*** Unknown syntax: {line}")
            return


if __name__ == '__main__':
    HBNBCommand().cmdloop()

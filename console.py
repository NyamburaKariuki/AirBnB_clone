#!/usr/bin/python3
"""defines the HBnB class for the console"""


import re
import cmd
import models
from shlex import split
from models.__init__ import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


def parse(arg):
    braces = re.search(r"\{(.*?)\}", arg)
    brackets = re.search(r"\[(.*?)\]", arg)
    if braces is None:
        if brackets is None:
            return [i.strip(",") for i in split(arg)]
        else:
            lex = split(arg[:brackets.span()[0]])
            ret1 = [i.strip(",") for i in lex]
            retl.append(brackets.group())
            return retl
    else:
        lex = split(arg[:braces.span()[0]])
        retl = [i.strip(",") for i in lex]
        retl.append(braces.group())
        return ret1
    
class HBNBCommand(cmd.Cmd):
    """Defines the HolbertonBnB command interpreter"""
    prompt = "(hbnb) "
    __classes = {
            "BaseModel",
            "User",
            "State",
            "City",
            "Place",
            "Amenity",
            "Review",
        }

    def default(self, arg):
        """defaul cmd behavior when prompt is invalid"""
        arumentdict = {
                "all": self.do_all,
                "destroy": do_destroy,
                "count": self.do_count,
                "show": self.do_show,
                "update": self.do_update
        }
        match = re.search(r"\.", arg)
        if match is not None:
            argl = [arg[:match.span()[0]], arg[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", argl[1])
            if match is not None:
                command = [argl[1][:match.span()[0]], match.group()[1:-1]]
                if command[0] in argumentdict.keys():
                    call = "{} {}".format(argl[0], command[1])
                    return argumentdict[command[0]](call)
        print("*** Unknown syntax: {}".format(arg))
        return

    def do_quit(self, args):
        """quit command to exit the program"""
        return True

    def do_EOF(self, line):
        """command to catch errors"""
        print("")
        return True

    def emptyline(self):
        """when an empty line is entered, shouldn't do anything"""
        pass

    def do_create(self, arg):
        """create a new class instance and prints it's id"""
        arg1 = parse(arg)
        if len(arg1) == 0:
            print("** class name missing **")
        if arg1[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            print(eval(arg1[0])().id)
            storage.save()

    def do_show(self, arg):
        """show the string rep of a class instance of a given id"""
        arg1 = parse(arg)
        dictionary = storage.all()
        if len(arg1) == 0:
            print("** class doesn't exist **")
        if len(arg1) == 1:
            print("** instance id missing **")
        if argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        if "{}.{}".format(argl[0], argl[1]) not in dictionary:
            print("** no instance found **")
        else:
            print(dictionary["{}.{}".format(argl[0], argl[1])])

    def do_destroy(self, arg):
        """delete a class instance of a given id"""
        dictionary = parse(arg)
        arg1 = parse(arg)
        if len(argl) == 0:
            print("** class name missing **")
        if len(argl) == 1:
            print("** instance id missing **")
        if argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        if "{}.{}".format(argl[0], argl[1]) not in dictionary.keys():
            print("** no instance found **")
        else:
            del dictionary["{}.{}".format(argl[0], argl[1])]
            storage.save()

    def do_all(self, arg):
        """
        display string rep of all instances of a given class
        If no class is specifies, displays all instanciated objects
        """
        arg1 = parse(arg)
        if len(arg1) > 0 and arg1[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            objdict = []
            for obj in storage.all().values():
                if arg1[0] == obj.__class__.__name__ and len(arg1) > 0:
                    objdict.append(obj.__str__())
                if len(arg1) == 0:
                    objdict.append(obj.__str__())
            print(objdict)

    def do_count(self, arg):
        """retrieve the number of instances in a given class"""
        arg1 = parse(arg)
        counter = 0
        for obj in storage.all().values():
            if arg1[0] == obj.__class__.__name__:
                counter += 1
        print(counter)

    def do_update(self, arg):
        """
        update a class instance of a given id by adding or updating
        a given attribute key/value pair or dictionary
        """
        arg1 = pasre(arg)
        dictionary = storage.all()
        if len(arg1) == 0:
            print("** class name missing **")
            return False
        if len(argl) == 1:
            print("** instance id missing **")
            return False
        if argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(argl) == 2:
            print("** attribute name missing **")
            return False
        if "{}.{}".format(argl[0], argl[1]) not in dictionary.keys():
            print("** no instance found **")
            return False
        if len(argl) == 3:
            try:
                type(eval(arg1[2])) != dict
            except NameError:
                print("** value missing **")
                return False
        if len(arg1) == 4:
            obj = dictionary["{}.{}".format(argl[0], argl[1])]
            if arg1[2] in obj.__class__.__dict__.keys():
                valtype = type(obj.__class__.__dict__[arg1[2]])
                obj.__dict__[argl[2]] = valtype(argl[3])
            else:
                obj.__dict__[argl[2]] = argl[3]
        elif type(eval(argl[2])) == dict:
            obj = dictionary["{}.{}".format(argl[0], argl[1])]
            for key, value in eval(argl[2]).items():
                if (key in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[key]) in {str, int, float}):
                    valtype = type(obj.__class__.__dict__[key])
                    obj.__dict__[key] = valtype(value)
                else:
                    obj.__dict__[key] = value
                storage.save()

    if __name__ == '__main__':
        HBNBCommand().cmdloop()

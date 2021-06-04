import pickle
from lib.convertor.convertor import to_dict, from_dict


class PickleParser:
    def dumps(obj):
        """python object -> string"""
        try:
            return pickle.dumps(to_dict(obj))
        except pickle.PicklingError as e:
            print("Error: wrong type in dumps (PICKLE)", e)

    def loads(s):
        """string -> python object"""
        try:
            return from_dict(pickle.loads(s))
        except pickle.UnpicklingError as e:
            print("Error in loads (PICKLE)", e)

    def dump(obj, fp="test.pickle"):
        """python object -> file"""
        with open(fp, "wb") as file:
            try:
                return pickle.dump(to_dict(obj), file)
            except pickle.PicklingError as e:
                print("Error: wrong type in dump (PICKLE)", e)

    def load(fp="test.pickle"):
        """file -> python object"""
        with open(fp, "rb") as file:
            try:
                return from_dict(pickle.load(file))
            except pickle.UnpicklingError as e:
                print("Error in load (PICKLE)", e)

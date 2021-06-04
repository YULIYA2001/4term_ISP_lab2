import pytomlpp
from lib.convertor.convertor import to_dict, from_dict


class TomlParser:

    def dumps(obj):
        """python object -> string"""
        try:
            return pytomlpp.dumps(to_dict(obj))
        except pytomlpp.DecodeError as e:
            print("Error in loads (TOML)", e)
        except TypeError as e:
            print("Error wrong type in dumps (TOML)", e)

    def loads(s):
        """string -> python object"""
        try:
            return from_dict(pytomlpp.loads(s))
        except pytomlpp.DecodeError as e:
            print("Error in loads (TOML)", e)
        except TypeError as e:
            print("Error in load (TOML)", e)

    def dump(obj, fp="test.toml"):
        """python object -> file"""
        with open(fp, 'w') as file:
            try:
                pytomlpp.dump(to_dict(obj), file)
            except pytomlpp.DecodeError as e:
                print("Error in loads (TOML)", e)
            except TypeError as e:
                print("Error wrong type in dump (TOML)", e)


    def load(fp="test.toml"):
        """file -> python object"""
        with open(fp, 'r') as file:
            try:
                return from_dict(pytomlpp.load(file))
            except pytomlpp.DecodeError as e:
                print("Error in load (TOML)", e)
            except TypeError as e:
                print("Error in load (TOML)", e)

#if __name__ == "__main__":
#    d = {'user': {'name': 'Bob', 'age': 10}}
#    path = Path().absolute()
#    TomlParser.dump(d, '/home/yuliya/ISP/lab2/unittests/test.toml')
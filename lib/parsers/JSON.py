import json
from lib.convertor.convertor import to_dict, from_dict


class JsonParser:

    def dumps(obj):
        """python object -> string"""
        try:
            return json.dumps(to_dict(obj))
        except json.JSONDecodeError:
            print("Error wrong type in dumps (JSON)")

    def loads(s):
        """string -> python object"""
        try:
            return from_dict(json.loads(s))
        except json.JSONDecodeError:
            print("Error in loads (JSON)")

    def dump(obj, fp="test.json"):
        """python object -> file"""
        with open(fp, 'w') as file:
            #try:
            #    return json.dump(to_dict(obj), fp)
            #except json.JSONDecodeError:
            #    print("Error wrong type in dump (JSON)")
            file.write(JsonParser.dumps(obj))

    def load(fp="test.json"):
        """file -> python object"""
        with open(fp, 'r') as file:
            try:
                return from_dict(json.load(file))
            except json.JSONDecodeError:
                print("Error in load (JSON)")

#from pathlib import Path
#
#if __name__ == "__main__":
#    d = {'user': {'name': 'Bob', 'age': 10}}
#    path = Path().absolute()
#    JsonParser.dump(d, '/home/yuliya/ISP/lab2/unittests/test.json')
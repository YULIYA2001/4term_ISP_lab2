import yaml
from lib.convertor.convertor import to_dict, from_dict


class YamlParser:

    def dumps(obj):
        """python object -> string"""
        try:
            return yaml.dump(to_dict(obj))
        except yaml.YAMLError as e:
            print("Error: wrong type in dumps (YAML)", e)

    def loads(s):
        """string -> python object"""
        try:
            return from_dict(yaml.load(s, Loader=yaml.FullLoader))
        except yaml.YAMLError as e:
            print("Error in loads (YAML)", e)

    def dump(obj, fp="test.yaml"):
        """python object -> file"""
        with open(fp, 'w') as file:
            yaml.dump(to_dict(obj), file)
        #    try:
        #        return yaml.dump(to_dict(obj), file)
        #    except yaml.YAMLError as e:
        #        print("Error: wrong type in dump (YAML)", e)


    def load(fp="test.yaml"):
        """file -> python object"""
        with open(fp, 'r') as file:
            try:
                return from_dict(yaml.load(file, Loader=yaml.FullLoader))
            except yaml.YAMLError as e:
                print("Error in load (YAML)", e)
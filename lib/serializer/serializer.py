from lib.parsers.JSON import JsonParser
from lib.parsers.PICKLE import PickleParser
from lib.parsers.TOML import TomlParser
from lib.parsers.YAML import YamlParser


def create_serializer(name: str):
    if name.lower() == ".json":
        return JsonParser
    elif name.lower() == ".pickle":
        return PickleParser
    elif name.lower() == ".toml":
        return TomlParser
    elif name.lower() == ".yaml":
        return YamlParser
    else:
        raise TypeError("Wrong file extension")

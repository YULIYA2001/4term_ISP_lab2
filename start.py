#!usr/bin/python3

import argparse
import configparser
from pathlib import Path
from lib.serializer.serializer import create_serializer


def serialize(new_format, fp):
    serializer = create_serializer(new_format)
    try:
        old_format = Path(fp).suffix
        if old_format == new_format:
            return
        deserializer = create_serializer(old_format)
        path = Path(fp)
        deserialized = deserializer.load(fp)
        serializer.dump(deserialized, Path(path.parent, f"{path.stem}{new_format}"))
    except FileNotFoundError as ex:
        print(ex)


def main():
    parser = argparse.ArgumentParser(description='convert to json/pickle/toml/yaml')
    parser.add_argument("-c", "--config", dest="configuration_file", help="configuration file path")
    parser.add_argument("-f", "--format", dest="new_format", help="new file format")
    parser.add_argument("-p", "--path", dest="file_path", help="path to your file")

    args = parser.parse_args()
    if args.configuration_file is not None:
        configuration = configparser.ConfigParser()
        try:
            configuration.read(args.configuration_file)
            serialize(configuration["configurations"]["new_format"], configuration["configurations"]["file_path"])
        except KeyError:
            print("invalid file")
    else:
        if args.new_format and args.file_path:
            serialize(args.new_format, args.file_path)
        else:
            raise TypeError("invalid parameters")


main()

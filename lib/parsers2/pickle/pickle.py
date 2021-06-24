import pickle


def dumps(obj):
    return pickle.dumps(obj)


def dump(obj, fp):
    s = dumps(obj).decode(encoding='unicode_escape')
    fp.write(s)


def loads(temp_str):
    return pickle.loads(temp_str)


def load(fp):
    return loads(fp.read())

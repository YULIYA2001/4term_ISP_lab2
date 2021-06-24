import re

from .resources import FLOAT_REGEX, INT_REGEX, STR_REGEX, DICT_REGEX, LIST_REGEX


def dump(obj, fp):
    s = dumps(obj)
    fp.write(s)


def load(fp):
    return loads(fp.read())


def dumps(obj):
    if obj is None:
        return "null"
    elif isinstance(obj, bool):
        return str(obj).lower()
    elif isinstance(obj, (int, float)):
        return str(obj)
    elif isinstance(obj, str):
        return "\"" + obj.replace('\\', '\\\\').replace('\n', '\\n') + "\""
    elif isinstance(obj, list):
        return f"[{','.join(dumps(o) for o in obj)}]"
    elif isinstance(obj, dict):
        return "{" + ",".join(f"\"{key}\":{dumps(val)}" for key, val in obj.items()) + "}"
    else:
        raise ValueError(f"Wrong type {type(obj)}")


def loads(s):
    s = s.strip("\n ")
    if s == "null":
        return None
    elif s == "false" or s == "true":
        return s[0] == 't'
    elif re.fullmatch(INT_REGEX, s):
        return int(s)
    elif re.fullmatch(FLOAT_REGEX, s):
        return float(s)
    elif re.fullmatch(DICT_REGEX, s):
        a = {}
        for ss in split(re.fullmatch(DICT_REGEX, s).group(1), ','):
            key, value = tuple(split(ss, ':'))
            a[loads(key)] = loads(value)
        return a
    elif re.fullmatch(LIST_REGEX, s):
        return [loads(ss) for ss in split(re.fullmatch(LIST_REGEX, s).group(1), ',')]
    elif re.fullmatch(STR_REGEX, s):
        return re.fullmatch(STR_REGEX, s).group(1).replace('\\n', '\n').replace('\\\\', '\\')
    else:
        raise ValueError(f"Wrong string \"{s}\"")


def split(s, mark):
    a = []
    depth = 0
    tmp = ""
    in_str = False
    marks = 0
    for i in range(len(s)):
        if is_quotation(s, i):
            in_str = not in_str
        if not in_str:
            if s[i] == '[' or s[i] == '{':
                depth += 1
            elif s[i] == ']' or s[i] == '}':
                depth -= 1
        if s[i] == mark and depth == 0 and not in_str:
            a.append(tmp)
            tmp = ""
            marks += 1
        else:
            tmp += s[i]
    if tmp.strip("\n ") != "":
        a.append(tmp)
    return a


def is_quotation(s, ind):
    if s[ind] != "\"":
        return False
    ind -= 1
    cnt = 0
    while ind >= 0 and s[ind] == "\\":
        ind -= 1
        cnt += 1
    return cnt % 2 == 0

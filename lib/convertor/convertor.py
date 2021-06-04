import builtins
import inspect
from types import FunctionType, CodeType, LambdaType

simple = (int, float, str, bool)


def __func_to_dict(py_func):
    res = {"__type__": "function"}
    if inspect.ismethod(py_func):
        py_func = py_func.__func__
    res["__name__"] = py_func.__name__
    globs = __take_globs(py_func)
    res["__globals__"] = __convert_l_t_d(globs)
    args = {}
    for (key, value) in inspect.getmembers(py_func.__code__):
        if key.startswith("co_"):
            if isinstance(value, bytes):
                value = list(value)
            if isinstance(value, (list, tuple, dict)):
                converted_vals = []
                for val in value:
                    if val is not None:
                        converted_vals.append(to_dict(val))
                    else:
                        converted_vals.append("none")
                args[key] = converted_vals
                continue
            args[key] = value
    res["__args__"] = args
    return res


def __take_globs(func):
    globs = {}
    for global_var in func.__code__.co_names:
        if global_var in func.__globals__:
            globs[global_var] = func.__globals__[global_var]
    return globs


def __class_to_dict(py_obj):
    res = {'__type__': 'class', '__name__': py_obj.__name__}
    for attr in dir(py_obj):
        if attr == "__init__":
            attr_value = getattr(py_obj, attr)
            res[attr] = __func_to_dict(attr_value)
        if not attr.startswith('__'):
            attr_value = getattr(py_obj, attr)
            res[attr] = to_dict(attr_value)
    return res


def __convert_l_t_d(py_obj):
    if isinstance(py_obj, (list, tuple)):
        res = []
        for value in py_obj:
            if value is None:
                res.append("none")
            res.append(to_dict(value))
        return res
    elif isinstance(py_obj, dict):
        res = {}
        for key, value in py_obj.items():
            res[key] = to_dict(value)
        return res


def __object_to_dict(py_obj):
    res = {"__type__": "object", "__class__": py_obj.__class__.__name__}
    for attr in dir(py_obj):
        if not attr.startswith("__"):
            value = to_dict(getattr(py_obj, attr))
            res[attr] = value
    return res


def to_dict(py_obj):
    if isinstance(py_obj, simple):
        return py_obj
    elif inspect.isfunction(py_obj) or inspect.ismethod(py_obj) or isinstance(py_obj, LambdaType):
        return __func_to_dict(py_obj)
    elif inspect.iscode(py_obj):
        # inner (nested) function to dict
        return __func_to_dict(FunctionType(py_obj, {}))
    elif inspect.isclass(py_obj):
        return __class_to_dict(py_obj)
    elif isinstance(py_obj, (list, tuple, dict)):
        return __convert_l_t_d(py_obj)
    else:
        return __object_to_dict(py_obj)


def __func_from_dict(f_func):
    args = f_func["__args__"]
    globs = f_func["__globals__"]
    globs["__builtins__"] = builtins
    for key in f_func["__globals__"]:
        if key in args["co_names"]:
            globs[key] = from_dict(f_func["__globals__"][key])

    consts = []
    for val in list(args["co_consts"]):
        func = from_dict(val)
        if inspect.isfunction(func) or inspect.ismethod(func) or isinstance(func, LambdaType):
            val = from_dict(val)
            consts.append(val.__code__)
            continue
        consts.append(val)
    args["co_consts"] = consts

    for val in args:
        if isinstance(args[val], (list, tuple, dict)):
            lst = []
            for value in args[val]:
                if value == "none":
                    lst.append(None)
                else:
                    lst.append(value)
            args[val] = lst

    code = CodeType(args['co_argcount'],
                    args['co_posonlyargcount'],
                    args['co_kwonlyargcount'],
                    args['co_nlocals'],
                    args['co_stacksize'],
                    args['co_flags'],
                    bytes(args['co_code']),
                    tuple(args['co_consts']),
                    tuple(args['co_names']),
                    tuple(args['co_varnames']),
                    args['co_filename'],
                    args['co_name'],
                    args['co_firstlineno'],
                    bytes(args['co_lnotab']),
                    tuple(args['co_freevars']),
                    tuple(args['co_cellvars']))
    return FunctionType(code, globs)


def __class_from_dict(f_obj):
    dct = {}
    for attr, val in f_obj.items():
        dct[attr] = from_dict(val)
    return type(f_obj["__name__"], (), dct)


def __deconvert_l_t_d(f_obj):
    if isinstance(f_obj, (list, tuple)):
        res = []
        for value in f_obj:
            if value == "none":
                res.append(None)
            res.append(from_dict(value))
        return res
    elif isinstance(f_obj, dict):
        res = {}
        for key, value in f_obj.items():
            res[key] = from_dict(value)
        return res


def __object_from_dict(f_obj):
    meta = type(f_obj.get("__class__"), (), {})
    res = meta()
    for key, value in f_obj.items():
        if key == '__class__':
            continue
        setattr(res, key, from_dict(value))
    return res


def from_dict(f_obj):
    if isinstance(f_obj, simple):
        return f_obj
    elif isinstance(f_obj, dict):
        if "function" in f_obj.values():
            return __func_from_dict(f_obj)
        elif "object" in f_obj.values():
            return __object_from_dict(f_obj)
        elif "class" in f_obj.values():
            return __class_from_dict(f_obj)
        else:
            return __deconvert_l_t_d(f_obj)
    elif isinstance(f_obj, (list, tuple, dict)):
        return __deconvert_l_t_d(f_obj)

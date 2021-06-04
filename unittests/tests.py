import unittest
from lib.serializer.serializer import create_serializer


def add(x, y):
    return x + y


mul = lambda x, y: x * y


def outer_func():
    def inner_func():
        return "Hello, World!"
    inner_func()


class Auto:
    mark = 'BMV'
    engine_value = 2.0

    def __init__(self, mark, eng_val):
        self.mark = mark
        self.components = ['wheels', 'body', 'engine']
        self.engine_value = eng_val

    def noise(self):
       return "Rrrrr. I am {:}. My engine value is {:} liter(s)".format(self.mark, self.engine_value)


car = Auto('BMV', 2.5)


class TestFunc(unittest.TestCase):
    format = [".json", ".pickle", ".toml", ".yaml"]

    def test_str(self):
        for val in self.format:
            in_format = create_serializer(val).dumps(add)
            in_python = create_serializer(val).loads(in_format)
            self.assertEqual(in_python(1, 2), add(1, 2))

    def test_file(self):
        for val in self.format:
            create_serializer(val).dump(add)
            in_python = create_serializer(val).load()
            self.assertEqual(in_python(2, -2), add(2, -2))


class TestLambda(unittest.TestCase):
    format = [".json", ".pickle", ".toml", ".yaml"]

    def test_str(self):
        for val in self.format:
            in_format = create_serializer(val).dumps(mul)
            in_python = create_serializer(val).loads(in_format)
            self.assertEqual(in_python(4, 2), mul(4, 2))

    def test_file(self):
        for val in self.format:
            create_serializer(val).dump(mul)
            in_python = create_serializer(val).load()
            self.assertEqual(in_python(2, -3), mul(2, -3))


class TestInnerFunction(unittest.TestCase):
    format = [".json", ".pickle", ".toml", ".yaml"]

    def test_str(self):
        for val in self.format:
            in_format = create_serializer(val).dumps(outer_func)
            in_python = create_serializer(val).loads(in_format)
            self.assertEqual(in_python(), outer_func())

    def test_file(self):
        for val in self.format:
            create_serializer(val).dump(outer_func)
            in_python = create_serializer(val).load()
            self.assertEqual(in_python(), outer_func())


class TestObject(unittest.TestCase):
    format = [".json", ".pickle", ".toml", ".yaml"]

    def test_str(self):
        for val in self.format:
            in_format = create_serializer(val).dumps(car)
            in_python = create_serializer(val).loads(in_format)
            self.assertEqual(in_python.noise(in_python), car.noise())
            self.assertEqual(in_python.components, car.components)
            self.assertEqual(in_python.mark, car.mark)
            self.assertEqual(in_python.engine_value, car.engine_value)

    def test_file(self):
        for val in self.format:
            create_serializer(val).dump(car)
            in_python = create_serializer(val).load()
            self.assertEqual(in_python.noise(in_python), car.noise())
            self.assertEqual(in_python.components, car.components)
            self.assertEqual(in_python.mark, car.mark)
            self.assertEqual(in_python.engine_value, car.engine_value)


class TestClass(unittest.TestCase):
    format = [".json", ".pickle", ".toml", ".yaml"]

    def test_str(self):
        for val in self.format:
            in_format = create_serializer(val).dumps(Auto)
            in_python = create_serializer(val).loads(in_format)
            real_auto = Auto('Audi', 2.7)
            deser_auto = in_python('Audi', 2.7)
            self.assertEqual(real_auto.noise(), deser_auto.noise())
            self.assertEqual(real_auto.components, deser_auto.components)
            self.assertEqual(real_auto.mark, deser_auto.mark)
            self.assertEqual(real_auto.engine_value, deser_auto.engine_value)

    def test_file(self):
        for val in self.format:
            create_serializer(val).dump(Auto)
            in_python = create_serializer(val).load()
            real_auto = Auto('Honda', 2.3)
            deser_auto = in_python('Honda', 2.3)
            self.assertEqual(real_auto.noise(), deser_auto.noise())
            self.assertEqual(real_auto.components, deser_auto.components)
            self.assertEqual(real_auto.mark, deser_auto.mark)
            self.assertEqual(real_auto.engine_value, deser_auto.engine_value)


if __name__ == "__main__":
    unittest.main()

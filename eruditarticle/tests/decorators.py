import os
import pytest


def with_fixtures(path, object_type):
    """ Class decorator that adds a ``test_objects`` dictionary to
    the test case.

    Loads all the objects in ``path`` and instantiates the corresponding
    ``object_types``
    """

    def decorator(cls):
        @pytest.fixture(autouse=True)
        def build_fixtures(self, *args, **kwargs):
            self.wrapped = cls(*args, **kwargs)
            self.test_objects = _get_test_objects(path, object_type)

        cls.build_fixtures = build_fixtures
        return cls
    return decorator


def with_value(test_object, method, *args, **kwargs):
    """ Test function decorator that calls the specified method
    on the test_object and pass the value to the test

    All positional and keywords arguments passed to the ``with_value``
    decorator will be passed to ``method``

    :param test_object: the object on which to call the method
    :param method: the method to call
    :param args: positional arguments to pass to ``method``
    :param kwargs: keyword arguments to pass to ``method``
    """
    def decorator(func):
        def wrapper(self):
            object_method = getattr(self.test_objects[test_object], method)
            results = object_method(*args, **kwargs)
            return func(self, results)
        return wrapper
    return decorator


def _get_test_objects(objects_path, object_type):
    """
    Loads all the test_objects in object_path and store them
    in a dictionary.

    Each key/value pair of the dictionary is

        key: filename of the object
        value: an instance of self.object_type

        :param objects_path: the path of the objects
        :param object_type: the object type
        :returns: a dictionary of the objects in path
    """
    test_objects = {}
    for filename in os.listdir(path=objects_path):
        if not filename.endswith('xml'):
            continue
        path = "{}/{}".format(objects_path, filename)

        with open(path, 'rb') as test_xml:
            test_objects[filename] = object_type(
                test_xml.read()
            )
    return test_objects

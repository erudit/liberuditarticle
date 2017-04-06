import os


def ea_value(filename, value, *args, **kwargs):
    def decorator(func):
        def wrapper(self):
            method = getattr(self.test_objects[filename], value)
            results = method(*args, **kwargs)
            return func(self, results)
        return wrapper
    return decorator


class BaseTestCase(object):
    def setup(self):
        """ Populates the test_objects dictionary

        Loads all the test_objects in object_path and store them
        in the test_objects dictionary.

        Each key/value pair of the test_objects dictionary is
            key: filename of the object
            value: an instance of self.object_type

        This TestCase assumes that all the test objects in
        directory `objects_path` are of the same type."""

        self.test_objects = {}

        for filename in os.listdir(path=self.objects_path):
            if not filename.endswith('xml'):
                continue
            path = "{}/{}".format(self.objects_path, filename)

            with open(path, 'rb') as test_xml:
                self.test_objects[filename] = self.object_type(
                    test_xml.read()
                )

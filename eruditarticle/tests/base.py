import os


def with_value(test_object, method, *args, **kwargs):
    """ Test function decorator that calls the specified method
    on the test_object and pass the value to the test

    :param test_object: the object on which to call the method
    :param method: the method to call
    """
    def decorator(func):
        def wrapper(self):
            object_method = getattr(self.test_objects[test_object], method)
            results = object_method(*args, **kwargs)
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

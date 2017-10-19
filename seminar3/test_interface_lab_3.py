
import sys
import unittest
import importlib
import collections

try:
    import mock
except ImportError:
    try:
        from unittest import mock
    except ImportError:
        mock = None

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

try:
    str_type = basestring
    int_type = (int, long)
except NameError:
    str_type = str
    int_type = int


# uncomment the line below and change the path specified
# sys.path.insert(0, r'path_to_solution_folder')


class InterfaceTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if mock is None:
            print('"mock" is not imported. cannot check stdout')

    def setUp(self):
        self._stdout_mock = self._setup_stdout_mock()

    def _setup_stdout_mock(self):
        if mock is None:
            return None

        patcher = mock.patch('sys.stdout', new=StringIO())
        patcher.start()
        self.addCleanup(patcher.stop)
        return patcher.new

    def _check_stdout_empty(self, file_name):
        if self._stdout_mock is not None:
            self.assertFalse(self._stdout_mock.getvalue(),
                             'no prints to console are allowed in "%s"' % file_name)

    def _load_function(self, task_idx, file_name, func_names):
        try:
            loaded_task = importlib.import_module(file_name)
        except ImportError:
            self.fail('cannot import task #%d solution - no file "%s"' % (task_idx, file_name))

        func_names = (func_names, ) if isinstance(func_names, str_type) else func_names
        loaded_functions = list(filter(None, (getattr(loaded_task, func_name, None) for func_name in func_names)))

        self.assertEqual(1, len(loaded_functions),
                         'cannot import task #%d solution - only one of function(-s) "%s" must be in file "%s"'
                         % (task_idx, file_name, func_names))

        return loaded_functions[0]

    def test_hist(self):
        f = self._load_function(0, 'hist', 'distribute')
        self.assertIsInstance(f([1, 2, 3], 1), list)

    def test_big_number(self):
        f = self._load_function(0, 'big_number', 'index')
        self.assertIsInstance(f('123', 1, 5), tuple)
        self._check_stdout_empty('big_number')

    def test_british(self):
        f = self._load_function(0, 'british', 'shuffle')
        self.assertIsInstance(f('123', True), str_type)
        self._check_stdout_empty('british')

if __name__ == '__main__':
    unittest.main()

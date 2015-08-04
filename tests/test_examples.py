import pyexcel as pe
from _compact import OrderedDict, execfile
from nose.tools import raises
import glob2
import os


BLACK_LIST = ['pyexcel_server', 'import_xls_into_database']

class TestAllExamples:
    def test_them(self):
        base = os.getcwd()
        example_files = glob2.glob(os.path.join('examples', '**', '*.py'))
        file_registry = {}
        for abs_file_path in example_files:
            for item in BLACK_LIST:
                if item in abs_file_path:
                    continue
            path, file_name = os.path.split(abs_file_path)
            if path not in file_registry:
                file_registry[path] = [file_name]
            else:
                file_registry[path].append(file_name)

        for path in file_registry:
            test_directory = os.path.join(base, path)
            os.chdir(test_directory)
            for file_name in file_registry[path]:
                try:
                    execfile(file_name)
                except:
                    os.system('python '+ file_name)
        os.chdir(base)

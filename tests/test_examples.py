import glob2
import os
import imp


def load_from_file(mod_name, file_ext):
    func_inst = None
    py_mod = None
    expected_main = 'main'

    #if file_ext.lower() == '.py':
    py_mod = imp.load_source(mod_name, os.path.join(mod_name, file_ext))

    #elif file_ext.lower() == '.pyc':
    #    py_mod = imp.load_compiled(mod_name, os.join(mod_name, file_ext))

    if py_mod is not None and hasattr(py_mod, expected_main):
        func_inst = getattr(py_mod, expected_main)

    return func_inst


class TestAllExamples:
    def test_them(self):
        example_files = glob2.glob(os.path.join('examples', '**', '*.py'))
        file_registry = {}
        for abs_file_path in example_files:
            if 'pyexcel_server.py' in abs_file_path:
                continue
            if '__init__.py' in abs_file_path:
                continue
            path, file_name = os.path.split(abs_file_path)
            if path not in file_registry:
                file_registry[path] = [file_name]
            else:
                file_registry[path].append(file_name)

        for path in file_registry:
            #test_directory = os.path.join(base, path)
            #os.chdir(test_directory)
            for file_name in file_registry[path]:
                print "###################"+os.path.join(path, file_name)
                fn = load_from_file(path, file_name)
                if fn is not None:
                    fn(path)
        #os.chdir(base)

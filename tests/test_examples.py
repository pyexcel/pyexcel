import glob2
import os
import imp
import json
import pyexcel as pe


def load_from_file(mod_name, file_ext, expected_main='main'):
    func_inst = None
    py_mod = None
    py_mod = imp.load_source(mod_name, os.path.join(mod_name, file_ext))
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
            for file_name in file_registry[path]:
                print("testing "+os.path.join(path, file_name))
                fn = load_from_file(path, file_name)
                if fn is not None:
                    fn(path)

class TestPyexcelServer:
    def setUp(self):
        app = load_from_file(os.path.join('examples', 'memoryfile'), 'pyexcel_server.py', 'app')
        self.app = app.test_client()

    def test_upload(self):
        data = [
            ['X', 'Y', 'Z'],
            [1, 2, 3],
            [4, 5, 6]
        ]
        expected = {
            "result": {
                "X": [
                    "1",
                    "4"
                ],
                "Y": [
                    "2",
                    "5"
                ],
                "Z": [
                    "3",
                    "6"
                ]
            }
        }
        io = pe.save_as(dest_file_type='csv', array=data)
        response = self.app.post('/upload', buffered=True,
                                 data = {"excel": (io, "test.csv")},
                                 content_type="multipart/form-data")
        assert json.loads(response.data) == expected

    def test_download(self):
        response = self.app.get('/download')
        ret = pe.get_array(file_type="csv", file_content=response.data)
        assert ret == [
            ["REVIEW_DATE","AUTHOR","ISBN","DISCOUNTED_PRICE"],
            ["1985/01/21","Douglas Adams",'0345391802','5.95'],
            ["1990/01/12","Douglas Hofstadter",'0465026567','9.95'],
            ["1998/07/15","Timothy \"The Parser\" Campbell",'0968411304','18.99'],
            ["1999/12/03","Richard Friedman",'0060630353','5.95'],
            ["2004/10/04","Randel Helms",'0879755725','4.5']
        ]


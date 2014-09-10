import os
from filters import HatReader
from utils import to_dict
from writers import Writer


__WARNING_TEXT__ = "We do not overwrite files"

def update_a_column(infilename, column_dicts, outfilename=None):
    default_out_file = "pyexcel_%s" % infilename
    if outfilename:
        default_out_file = outfilename
    if os.path.exists(default_out_file):
        raise NotImplementedError(__WARNING_TEXT__)
    r = HatReader(infilename)
    keys = column_dicts.keys()
    data = to_dict(r)
    for k in keys:
        if k in data:
            data[k] = column_dicts[k]
        else:
            print "Unkown column name: %s" % k
    w = Writer(default_out_file)
    w.write_hat_table(data)
    w.close()

def merge_files(file_array, outfilename="pyexcel_merged.csv"):
    """

    Assuming data file with column headers
    Constraints: only write the minimum number of rows
    """
    if os.path.exists(outfilename):
        raise NotImplementedError(__WARNING_TEXT__)
    content = {}
    for f in file_array:
        r = HatReader(f)
        content.update(to_dict(r))
    w = Writer(outfilename)
    w.write_hat_table(content)
    w.close()
    

def merge_two_files(file1, file2, outfilename="pyexcel_merged.csv"):
    """

    Assuming data file with column headers
    Constraints: only write the minimum number of rows
    """
    if os.path.exists(outfilename):
        raise NotImplementedError(__WARNING_TEXT__)
    files = [file1, file2]
    merge_files(files)
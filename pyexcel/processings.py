import os
from filters import HatReader
from utils import to_dict
from writers import Writer


def update_a_column(infilename, column_dicts, outfilename=None):
    default_out_file = "pyexcel_%s" % infilename
    if outfilename:
        default_out_file = outfilename
    if os.path.exists(default_out_file):
        raise NotImplementedError("We do not overwrite files")
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
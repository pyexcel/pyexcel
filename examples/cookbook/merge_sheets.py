import pyexcel
import glob
merged = pyexcel.Reader()
for file in glob.glob("*.ods"):
    merged += pyexcel.Reader(file)
writer = pyexcel.Writer("merged.csv")
writer.write_reader(merged)
writer.close()
class Writer:
    def __init__(self, file):
        self.f = open(file, "w")

    def write_row(self, array):
        self.f.write(",".join([str(x) for x in array])+"\n")

    def close(self):
        self.f.close()
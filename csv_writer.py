import csv


class CsvWriter:
    full_file_path = None
    header = None
    data = None
    header = None

    def __init__(self, file_path, header, dats):
        self.full_file_path = file_path
        self.data = dats
        self.header = header

    def create_csv(self):
        with open(self.full_file_path, 'w', encoding='UTF8', newline='') as fp:
            writer = csv.writer(fp)
            writer.writerow(self.header)
            writer.writerows(self.data)

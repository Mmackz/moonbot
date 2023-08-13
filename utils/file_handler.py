import csv

class FileHandler:
    def __init__(self, filepath):
        self.filepath = filepath

    def save_file(self, content):
        with open(self.filepath, 'wb') as file:
            file.write(content)

    def read_csv(self):
        with open(self.filepath, 'r') as file:
            reader = csv.reader(file)
            return list(reader)

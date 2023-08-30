import csv
import logging

class FileHandler:
    def __init__(self, filepath):
        self.filepath = filepath

    def save_file(self, content):
        try:
            with open(self.filepath, 'wb') as file:
                file.write(content)
            return True
        except Exception as e:
            logging.error(f"An error occurred while saving the file: {e}")
            return False

    def read_csv(self):
        with open(self.filepath, 'r') as file:
            reader = csv.reader(file)
            return list(reader)

import csv
from pathlib import Path
import shutil


def load_csv(csv_path):
    data_sheet = {}

    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)

        for row in reader:
            data_sheet[row['id']] = row

    return data_sheet


def del_folder(folder_path):
    folder_path = Path(folder_path)
    if folder_path.exists():
        shutil.rmtree(folder_path)


def del_file(file_path):
    file_path = Path(file_path)
    if file_path.exists():
        file_path.unlink()

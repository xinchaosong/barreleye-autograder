import os
import csv


def load_csv(csv_path):
    data_sheet = {}

    if not os.path.exists(csv_path):
        csv_path = os.path.join(os.path.dirname(__file__), csv_path)

    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)

        for row in reader:
            data_sheet[row['id']] = row

    return data_sheet

import csv
import json


# Програма для чтения txt
def read_txt_file(way: str) -> list:
    with open(way, 'r', encoding='utf-8') as file:
        data_list = file.read().split('\n')
    return data_list


# Програма для чтения csv
def read_csv(file_name: str) -> None:
    spisok_worker = []
    with open(file_name, 'r', newline='') as file:
        reader = csv.reader(file, delimiter=';')
        for row in reader:
            spisok_worker.append(', '.join(row))
    return spisok_worker


# Програма для чтения json
def read_json(file_name: str) -> None:
    with open(file_name, 'r',encoding='utf-8', newline='') as file:
        data = json.loads(file.read())
    return data


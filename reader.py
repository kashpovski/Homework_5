import json
import csv

path_users = "data/users.json"
path_books = "data/books.csv"
path_reference = "data/reference.json"
path_result = "result.json"


def read_file_json(path):
    with open(path, "r") as file:
        return json.load(file)


def read_file_csv(path):
    with open(path, "r") as file:
        for f in csv.DictReader(file):
            yield f


def create_file_result(path, data_1, data_2, schema):
    """Создание списка словарей пользователей из базы по шаблону
       Запись книжек из базы по шаблону в список словарей пользователей по принципу раздачи карт
    """
    result_users = []
    for i in data_1:
        string_result_users = {}
        for j in dict(*schema):
            string_result_users[j] = i.get(j, [])
        result_users.append(string_result_users)

    while True:
        for i in result_users:
            j = next(data_2, "end list")
            if j == "end list":
                break
            result_books = i["books"]
            string_result_books = {}
            for k in dict(*dict(*schema)["books"]):
                string_result_books[k] = j.get(k.capitalize())
            result_books.append(string_result_books)
            i["books"] = result_books
        else:
            continue
        break

    with open(path, "w") as file:
        json.dump(result_users, file, indent=4)


users = read_file_json(path_users)
books = read_file_csv(path_books)
reference = read_file_json(path_reference)
create_file_result(path_result, users, books, reference)

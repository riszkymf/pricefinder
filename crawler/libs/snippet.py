import os
from . import util


def open_file(filename):
    path = util.get_path(filename)
    with open(path, "r") as f:
        data = f.read()
        f.close()
    return data


def show_data(data):
    print(data.product_name)
    data = data.data
    for item in data:
        for key, value in item.items():
            print(key, ": ", value)
        print("\n")
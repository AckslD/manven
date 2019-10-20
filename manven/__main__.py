import os


def print_path_to_here():
    path_to_here = os.path.dirname(os.path.abspath(__file__))
    print(path_to_here)


print_path_to_here()

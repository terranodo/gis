import gisdata
import os


def load_test_data():
    gisdata_path = os.path.abspath(os.path.join(os.path.dirname(gisdata.__file__), ".."))
    print(gisdata_path)


if __name__ == "__main__":
    load_test_data()

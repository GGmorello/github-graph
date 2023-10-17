import time
import shutil
from os import listdir
from os.path import isfile, join, basename
from pathlib import Path

data_folder_path = "../data"
dest_folder_path = "input_files"

Path(dest_folder_path).mkdir(parents=True, exist_ok=True)

def move_file(path):
    shutil.copy(path, join(dest_folder_path, basename(path)))

def move_directory(path):
    shutil.copytree(path, join(dest_folder_path, basename(path)))

def import_files():
    for f in listdir(data_folder_path):
        if isfile(join(data_folder_path, f)):
            move_file(join(data_folder_path, f))
        else:
            move_directory(join(data_folder_path, f))

# Imports the scraped commits into the streaming input folder
if __name__ == "__main__":
    # TODO schedule import every 30s?
    import_files()
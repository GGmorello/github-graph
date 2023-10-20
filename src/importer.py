import time
import shutil
import re
from os import listdir
from os.path import isfile, isdir, join, basename, dirname, exists
from pathlib import Path

data_folder_path = "../data"
dest_folder_path = "input_files"
file_pattern_regex = r'^commits.json$'

Path(dest_folder_path).mkdir(parents=True, exist_ok=True)

def move_file(path):
    dir = basename(dirname(path))
    dest_dir = join(dest_folder_path, dir)
    dest = join(dest_dir, basename(path))
    if not exists(dest_dir):
        Path(dest_dir).mkdir(parents=True, exist_ok=True)
    shutil.copy(path, dest)

def import_files(dir):
    for f in listdir(dir):
        if isfile(join(dir, f)) and re.search(file_pattern_regex, f) != None:
            move_file(join(dir, f))
        elif isdir(join(dir, f)):
            import_files(join(dir, f))

# Imports the scraped commits into the streaming input folder
if __name__ == "__main__":
    import_files(data_folder_path)
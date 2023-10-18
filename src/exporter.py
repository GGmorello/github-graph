import time
import json
import re
import requests
from os import listdir
from os.path import isfile, join

visualizer_url = "http://127.0.0.1:5000"
output_file_path = "output_files"
file_pattern_regex = r'^part-[\w|-]+\.json$'

def send_file_contents(path):
    with open(path) as f:
        list = []
        for l in f.readlines():
            data = json.loads(l)
            list.append(data)
        print("sending content from file {} to server {}".format(path, visualizer_url))
        requests.post(visualizer_url + "/append", json = list)

def export_files():
    for f in listdir(output_file_path):
        if (isfile(join(output_file_path, f)) and
            re.search(file_pattern_regex, f) != None):
            send_file_contents(join(output_file_path, f))
            # time.sleep(0.3)

# Exports the output files from the stream to the visualization API
if __name__ == "__main__":
    # TODO schedule export repeatedly every 30s?
    export_files()
# integrate_jsons_fixing.py
# 미완성..
import os
import json
from datetime import datetime

rectangles = {
    "topLeft": {"x": 0, "y": 0},
    "bottomRight": {"x": 0, "y": 0},
    "label": ""
}

frames = {
    "src": "",
    "lines": [],
    "rectangles": [],
    "polygons": [],
    "polylines": [],
}

datasets = {"frames": [], "actions": []}

file_lists = []
file_times = []
latest_files = []

if os.path.exists('./total_datasets.json'):
    os.remove('./total_datasets.json')

for path, dirs, files in os.walk('.'):
    for filenames in files:
        file_lists.append(os.path.join(path, filenames))
        file_times.append(os.path.getmtime(os.path.join(path, filenames)))
    for filename in file_lists:
        if os.path.getmtime(filename) == max(file_times) \
                and filename.endswith(".json"):
            latest_files.append(filename)
    file_lists.clear()
    file_times.clear()

for filename in latest_files:
    with open(filename) as f:
        jsonfile = json.load(f)
        for json_index, jsons in enumerate(jsonfile["frames"]):
            for dataset_index, dataset in enumerate(datasets["frames"]):
                if jsons["src"] == dataset["src"]:
                    print("jsons[\"src\"]: ", jsons["src"])
                    for rectangle in jsons["rectangles"]:
                        datasets["frames"][dataset_index]["rectangles"].append(rectangle)
                    continue
            datasets["frames"].append(jsons)

with open('total_datasets.json', 'w') as outfile:
    outfile.write(json.dumps(datasets, indent=4))

#frame_index = next((index for (index, dicts) in enumerate(frame) if dicts["src"] == frame["src"]), None)
#2014-11-20_074640_000000050


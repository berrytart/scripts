# integrate_jsons.py
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

# 기존 total_datasets.json 파일이 존재한다면 제거
if os.path.exists('./total_datasets.json'):
    os.remove('./total_datasets.json')

"""
" 현재 스크립트가 저장된 위치로부터 모든 파일 탐색
"
" path: 현재 경로 (type: str)
" dirs: 모든 폴더 이름 (type: list)
" files: 모든 파일 이름 (type: list)
"""
for path, dirs, files in os.walk('.'):
    for filenames in files:
        
        # 파일 리스트에 추가
        file_lists.append(os.path.join(path, filenames))

        # 파일별 수정 날짜 리스트에 추가 
        file_times.append(os.path.getmtime(os.path.join(path, filenames)))

    for filename in file_lists:

        # 파일 순차 탐색하여 json 파일 중
        # 가장 최신파일 탐지하여 latest_files에 붙임
        if os.path.getmtime(filename) == max(file_times) \
                and filename.endswith(".json"):
            latest_files.append(filename)
    file_lists.clear()
    file_times.clear()

# 각 폴더별 최신 json load해서 datasets에 병합
for filename in latest_files:
    with open(filename) as f:
        jsonfile = json.load(f)
        for frames in jsonfile["frames"]:
            datasets["frames"].append(frames)

# src 이름순으로 정렬
datasets["frames"] = sorted(datasets["frames"], key=lambda k: k["src"])

# total_datasets.json 이라는 이름으로 파일 저장
with open('total_datasets.json', 'w') as outfile:
    outfile.write(json.dumps(datasets, indent=4))

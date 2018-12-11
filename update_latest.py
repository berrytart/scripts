# update_latest.py
import os
import json

total_jsons = {}
latest_datasets = {"frames": [], "actions": []}

# nested loop escape 용도
breaker = False

# total_datasets_fix.json 파일 열기
with open('total_datasets_fix.json') as infile:
    total_jsons = json.load(infile)

    # json의 frame 부분 loop
    for frames in total_jsons["frames"]:
        breaker = False

        """
        " 현재 스크립트가 저장된 위치로부터 모든 파일 탐색
        "
        " path: 현재 경로 (type: str)
        " dirs: 모든 폴더 이름 (type: list)
        " files: 모든 파일 이름 (type: list)
        """
        for path, dirs, files in os.walk('.'):
            for filenames in files:

                # json 파일내 src 이름과 파일 이름 같을 때
                # 해당 frame을 latest_dataset에 붙임
                if filenames == frames["src"]:
                    latest_datasets["frames"].append(frames)
                    breaker = True
                    break
            if breaker:
                break

# total_datasets_fix_latest.json 이라는 이름으로 파일 저장
with open('total_datasets_fix_latest.json', 'w') as outfile:
    outfile.write(json.dumps(latest_datasets, indent=4))

import os
import sys
import copy
import json

savefiles = ""

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
    "polylines": []
}

datasets = {"frames": [], "actions": []}

# 현재 디렉토리 위치에서 .txt 파일 검색
for files in os.listdir("."):
    if files.endswith(".txt"):
        savefiles = files.split('_')[1] + "_datasets.json"

        # txt 파일 열기
        with open(files) as f:
            frames["src"] = f.name.replace("labelData.txt", "leftImg8bit.png")
            
            # txt 파일 라인별로 읽음
            for line in f:
                
                # 띄어쓰기 단위로 문장 끊어 읽기
                # list 형식으로 저장
                val = line.split()

                # json 형식으로 사각형 정의
                rectangles["topLeft"]["x"] = int(float(val[4]))
                rectangles["topLeft"]["y"] = int(float(val[5]))
                rectangles["bottomRight"]["x"] = int(float(val[6]))
                rectangles["bottomRight"]["y"] = int(float(val[7]))
                rectangles["label"] = val[0]
                
                # 깊은 복사 수행
                frames["rectangles"].append(copy.deepcopy(rectangles))

            # 깊은 복사 수행    
            datasets["frames"].append(copy.deepcopy(frames))

            # frames dictionary flush
            frames["src"] = ""
            frames["rectangles"].clear()

# savefiles 변수에 저장된 이름으로 파일 저장
with open(savefiles, 'w') as outfile:
    # json.dump(datasets, outfile)
    outs = json.dumps(datasets, indent=4)
    outfile.write(outs)

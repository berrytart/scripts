# split_imgs2.py
import os
import json
import shutil

dirname = 1
file_counts = 0

datasets = {"frames": [], "actions": []}
dataset_part = {"frames": [], "actions": []}

# train_used_iou_rect_redefy.json 파일 열기
with open('test.json') as jsonfile:
    jsons = json.load(jsonfile)

    # src 이름순으로 정렬
    jsons["frames"] = sorted(jsons["frames"], key=lambda k: k["src"])

    """
    " 현재 스크립트가 저장된 위치로부터 모든 파일 탐색
    "
    " path: 현재 경로 (type: str)
    " dirs: 모든 폴더 이름 (type: list)
    " files: 모든 파일 이름 (type: list)
    """
    filenames = os.listdir('.')
    for filename in filenames:
        for frames in jsons["frames"]:
            if frames["src"] == filename:                
                # 폴더 명은 1부터 시작, 일정 갯수 설정하여 담기
                if file_counts == 40:
                    file_counts = 0
                    dirname += 1
                if not os.path.exists(str(dirname)):
                    os.mkdir(str(dirname))
                try:
                    if os.path.exists(filename):
                        shutil.move(filename, str(dirname))
                        file_counts += 1
                except shutil.Error:
                    break

    # 각 하위폴더 접근하여 담겨있는 png 파일명 참조후 json 파일 생성
    for filename in filenames:
        if os.path.isdir(filename):
            os.chdir(os.path.join('.', filename))
            pngnames = os.listdir('.')
            for pngname in pngnames:
                if pngname.endswith('.json'):
                    os.remove(pngname)
                for frames in jsons["frames"]:
                    if frames["src"] == pngname:
                        dataset_part["frames"].append(frames)
            savejson = os.getcwd() + '.json'
            with open(savejson, 'w') as parts:
                parts.write(json.dumps(dataset_part, indent=4))
            shutil.move(savejson, os.getcwd())
            dataset_part["frames"].clear()
            os.chdir('..')

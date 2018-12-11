# split_imgs.py
import os
import json
import shutil

# train_used_iou_rect_redefy.json 파일 열기
with open('train_used_iou_rect_redefy.json') as jsonfile:
    jsons = json.load(jsonfile)

    """
    " 현재 스크립트가 저장된 위치로부터 모든 파일 탐색
    "
    " path: 현재 경로 (type: str)
    " dirs: 모든 폴더 이름 (type: list)
    " files: 모든 파일 이름 (type: list)
    """
    for path, dirs, files in os.walk('.'):
        for frames in jsons["frames"]:
            for filename in files:
                if frames["src"] == filename:
                    splits = filename.split('_')
                    dirname = splits[1] + '_' + splits[2]
                    if not os.path.exists(dirname):
                        os.mkdir(dirname)
                    try:
                        shutil.move(filename, dirname)
                    except shutil.Error:
                        break
                        

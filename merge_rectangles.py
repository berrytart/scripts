# merge_rectangles.py
import copy
import json

new_rect = {
    "topLeft": {"x": 0, "y": 0},
    "bottomRight": {"x": 0, "y": 0},
    "label": ""
}

new_frames = {
    "src": "", 
    "lines": [], 
    "rectangles": [], 
    "polygons": [], 
    "polylines": []
}

new_datasets = {"frames": [], "actions": []}

def bb_intersection_over_union(boxA, boxB):
    # determine the (x, y)-coordinates of the intersection rectangle
    xA = max(boxA[0], boxB[0])
    yA = min(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = max(boxA[3], boxB[3])

    # compute the area of intersection rectangle
    interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)

    # compute the area of both the prediction and ground-truth
    # rectangles
    boxAArea = abs((boxA[2] - boxA[0] + 1) * (boxA[3] - boxA[1] + 1))
    boxBArea = abs((boxB[2] - boxB[0] + 1) * (boxB[3] - boxB[1] + 1))

    # compute the intersection over union by taking the intersection
    # area and dividing it by the sum of prediction + ground-truth
    # areas - the interesection area
    iou = interArea / float(boxAArea + boxBArea - interArea)

    # return the intersection over union value
    return iou

# total_datasets_iou.json 파일 열기
with open('total_datasets_iou.json') as f:
    jsons = json.load(f)

    # jsons dictionary에서 action list는 쓰지 않으므로 jsons의 frame 부분만 loop
    for frames in jsons["frames"]:
        new_frames["src"] = copy.deepcopy(frames["src"])
        new_rects = copy.deepcopy(frames["rectangles"])

        # 각 frame의 index 및 사각형 부분만 loop
        for j, rect_a in enumerate(frames["rectangles"]):
            box_a = [rect_a["topLeft"]["x"], \
                    rect_a["topLeft"]["y"], \
                    rect_a["bottomRight"]["x"], \
                    rect_a["bottomRight"]["y"]]
            for k, rect_b in enumerate(frames["rectangles"]):
                
                # 동일한 사각형일 경우 skip
                if j >= k:
                    continue
                box_b = [rect_b["topLeft"]["x"], \
                        rect_b["topLeft"]["y"], \
                        rect_b["bottomRight"]["x"], \
                        rect_b["bottomRight"]["y"]]
                # iou 계산
                iou = bb_intersection_over_union(box_a, box_b)

                # iou가 특정 기준 이상(여기서는 0.9)이며 사각형의 label 동일할 때
                # 중첩되는 영역 생성 및 기존 서로 중첩되는 사각형 제거
                if iou >= 0.8 and \
                        rect_a["label"].split('_')[0] \
                        == rect_b["label"].split('_')[0]:
                    Ltlx = rect_a["topLeft"]["x"]
                    Ltly = rect_a["topLeft"]["y"]
                    Lbrx = rect_a["bottomRight"]["x"]
                    Lbry = rect_a["bottomRight"]["y"]
                    Rtlx = rect_b["topLeft"]["x"]
                    Rtly = rect_b["topLeft"]["y"]
                    Rbrx = rect_b["bottomRight"]["x"]
                    Rbry = rect_b["bottomRight"]["y"]

                    # 중첩되는 영역 계산하여 새로운 사각형 생성
                    new_rect["topLeft"]["x"] = max(Ltlx, Rtlx)
                    new_rect["topLeft"]["y"] = max(Ltly, Rtly)
                    new_rect["bottomRight"]["x"] = min(Lbrx, Rbrx)
                    new_rect["bottomRight"]["y"] = min(Lbry, Rbry)
                    new_rect["label"] = rect_a["label"]

                    # 기존 서로 중첩되는 사각형 제거 후 새로운 사각형을 list에 삽입
                    for rects in new_rects:
                        if rect_a == rects or rect_b == rects:
                            new_rects.remove(rects)
                            break

                    if new_rect not in new_rects:
                        new_rects.append(new_rect)
                    continue
        # 사각형들을 new_frames에 복사
        new_frames["rectangles"] = new_rects

        # new_dataset에 깊은 복사
        new_datasets["frames"].append(copy.deepcopy(new_frames))

# total_datasets_iou_merged.json 이라는 이름으로 파일 저장
with open('total_datasets_iou_merged.json', 'w') as outfile:
    outfile.write(json.dumps(new_datasets, indent=4))

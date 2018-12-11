# concat_iou_to_label_entire.py
import json

new_rect = {
    "topLeft": {"x": 0, "y": 0},
    "bottomRight": {"x": 0, "y": 0},
    "label": ""
}

datasets = {"frames": [], "actions": []}

def bb_intersection_over_union(boxA, boxB):
    # determine the (x, y)-coordinates of the intersection rectangle
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])

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

# train.json 파일 열기
with open('train.json') as f:
    datasets = json.load(f)

    # datasets dictionary에서 action list는 쓰지 않으므로 datasets의 frame 부분만 loop
    for i, frames in enumerate(datasets["frames"]):

        # 각 frame의 index 및 사각형 부분만 loop
        for j, rect_a in enumerate(frames["rectangles"]):
            box_a = [rect_a["topLeft"]["x"], \
                    rect_a["topLeft"]["y"], \
                    rect_a["bottomRight"]["x"], \
                    rect_a["bottomRight"]["y"]]
            for k, rect_b in enumerate(frames["rectangles"]):

                # 동일한 사각형일 경우 skip
                if j == k:
                    continue
                box_b = [rect_b["topLeft"]["x"], \
                        rect_b["topLeft"]["y"], \
                        rect_b["bottomRight"]["x"], \
                        rect_b["bottomRight"]["y"]]

                # iou 계산
                iou = bb_intersection_over_union(box_a, box_b)

                # iou가 특정 기준 이상(여기서는 0.9)이며 사각형의 label 동일할 때
                # 중첩되는 영역 생성 및 기존 서로 중첩되는 사각형 제거
                if iou >= 0.9 and \
                        frames["rectangles"][j]["label"].split('_')[0] \
                        == frames["rectangles"][k]["label"].split('_')[0]:
                    Ltlx = frames["rectangles"][j]["topLeft"]["x"]
                    Ltly = frames["rectangles"][j]["topLeft"]["y"]
                    Lbrx = frames["rectangles"][j]["bottomRight"]["x"]
                    Lbry = frames["rectangles"][j]["bottomRight"]["y"]
                    Rtlx = frames["rectangles"][k]["topLeft"]["x"]
                    Rtly = frames["rectangles"][k]["topLeft"]["y"]
                    Rbrx = frames["rectangles"][k]["bottomRight"]["x"]
                    Rbry = frames["rectangles"][k]["bottomRight"]["y"]

                    # 중첩되는 영역 계산하여 새로운 사각형 생성
                    new_rect["topLeft"]["x"] = max(Ltlx, Rtlx)
                    new_rect["topLeft"]["y"] = min(Ltly, Rtly)
                    new_rect["bottomRight"]["x"] = min(Lbrx, Rbrx)
                    new_rect["bottomRight"]["y"] = max(Lbry, Rbry)
                    new_rect["label"] = frames["rectangles"][j]["label"]

                    # 기존 서로 중첩되는 사각형 제거 후 새로운 사각형을 list에 삽입
                    datasets["frames"][i]["rectangles"].pop(j)
                    datasets["frames"][i]["rectangles"].pop(k-1)
                    datasets["frames"][i]["rectangles"].insert(0, new_rect)
                    
                    if j > 0:
                        j -= 1
                    continue

                # 사각형끼리 중첩되는 부분 있을시 label 뒤에 iou 값 붙임
                if iou > 0:
                    area_a = (abs(box_a[0]-box_a[2])) * (abs(box_a[1]-box_a[3]))
                    area_b = (abs(box_b[0]-box_b[2])) * (abs(box_b[1]-box_b[3]))

                    # 사각형 넓이를 비교하여 넓이가 작을 경우 사진상에서 더욱 뒤에 있는 물체라 판단
                    # 넓이가 작은 사각형의 label에 iou 값 붙임
                    if area_a < area_b:
                        label_iou = frames["rectangles"][j]["label"].split('_')[0] \
                        + "_" + str(round(iou, 3))
                        frames["rectangles"][j]["label"] = label_iou
                        datasets["frames"][i]["rectangles"][j] = frames["rectangles"][j]
                    else:
                        label_iou = frames["rectangles"][k]["label"].split('_')[0] \
                        + "_" + str(round(iou, 3))
                        frames["rectangles"][k]["label"] = label_iou
                        datasets["frames"][i]["rectangles"][k] = frames["rectangles"][k]

            # 그 외 해당하지 않는 사각형들 다시 datasets에 저장
            datasets["frames"][i]["rectangles"][j] = frames["rectangles"][j]

# total_datasets_iou.json 이라는 이름으로 파일 저장
with open('total_datasets_iou.json', 'w') as outfile:
    outfile.write(json.dumps(datasets, indent=4))

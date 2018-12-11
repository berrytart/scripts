import json
import argparse
import numpy as np
import cv2
import os
'''
Regtangle을 img에 넣어서 저장
띄어쓰기 주의: 10번 줄에"＾"로 표시
rectangle_img.py＾C:/Users/KDU/Downloads/annotation/test/＾test.json
rectangle_img.py C:/Users/KDU/Downloads/annotation/test/ test.json
'''
drawing = False
ix, iy = -1, -1
font = cv2.FONT_HERSHEY_SIMPLEX


def readfile(filename):
  f = open(filename, 'r')
  js = json.loads(f.read())
  f.close()
  return js

parser = argparse.ArgumentParser()
parser.add_argument('root', type=str)
parser.add_argument('file', type=str)
args = parser.parse_args()

anno_root = args.root
anno_file = anno_root + args.file
dirname = args.root + 'result'#체크하고자 하는 디렉토리명

if not os.path.isdir(dirname): #디렉토리 유무 확인
  os.mkdir(dirname)  #없으면 생성하라.

anno_info = readfile(anno_file)

idx = 0

labels = ['Car', 'Pedestrian', 'Misc', 'Cyclist', 'Motorcyclist', 'Van', 'Truck', 'Bus', 'Person_sitting', 'Tram', 'Dontcare']

while idx < len(anno_info['frames']):
  img = cv2.imread(anno_root + anno_info['frames'][idx]['src'])
  for rect in anno_info['frames'][idx]['rectangles']:
    name = anno_info['frames'][idx]['src']
    xmin = rect['topLeft']['x']
    ymax = rect['topLeft']['y']
    xmax = rect['bottomRight']['x']
    ymin = rect['bottomRight']['y']
    label = rect['label']
    tl = (xmin, ymax)
    br = (xmax, ymin)
    if label not in labels:#Label이 다르면 보라색
      cv2.rectangle(img, tl, br, (255, 0, 255))
      cv2.putText(img, label, (xmin, ymin), font, 0.4, (255, 0, 255), 1, cv2.LINE_AA)
    if label == 'Car':
      cv2.rectangle(img, tl, br, (255, 0, 0))
      cv2.putText(img, label, (xmin, ymin), font, 0.4, (255, 0, 0), 1, cv2.LINE_AA)
    if label == 'Pedestrian':
      cv2.rectangle(img, tl, br, (0, 255, 0))
      cv2.putText(img, label, (xmin, ymin), font, 0.4, (0, 255, 0), 1, cv2.LINE_AA)
    if label == 'Misc':
      cv2.rectangle(img, tl, br, (0, 0, 0))
      cv2.putText(img, label, (xmin, ymin), font, 0.4, (0, 0, 0), 1, cv2.LINE_AA)
    if label == 'Cyclist':
      cv2.rectangle(img, tl, br, (0, 0, 255))
      cv2.putText(img, label, (xmin, ymin), font, 0.4, (0, 0, 255), 1, cv2.LINE_AA)
    if label == 'Motorcyclist':
      cv2.rectangle(img, tl, br, (0, 0, 255))
      cv2.putText(img, label, (xmin, ymin), font, 0.4, (0, 0, 255), 1, cv2.LINE_AA)
    if label == 'Van':
      cv2.rectangle(img, tl, br, (255, 0, 0))
      cv2.putText(img, label, (xmin, ymin), font, 0.4, (255, 0, 0), 1, cv2.LINE_AA)
    if label == 'Truck':
      cv2.rectangle(img, tl, br, (255, 0, 0))
      cv2.putText(img, label, (xmin, ymin), font, 0.4, (255, 0, 0), 1, cv2.LINE_AA)
    if label == 'Bus':
      cv2.rectangle(img, tl, br, (255, 0, 0))
      cv2.putText(img, label, (xmin, ymin), font, 0.4, (255, 0, 0), 1, cv2.LINE_AA)
    if label == 'Person_sitting':
      cv2.rectangle(img, tl, br, (0, 255, 0))
      cv2.putText(img, label, (xmin, ymin), font, 0.4, (0, 255, 0), 1, cv2.LINE_AA)
    if label == 'Tram':
      cv2.rectangle(img, tl, br, (255, 0, 0))
      cv2.putText(img, label, (xmin, ymin), font, 0.4, (255, 0, 0), 1, cv2.LINE_AA)
    if label == 'Dontcare':
      cv2.rectangle(img, tl, br, (255, 255, 255))
      cv2.putText(img, label, (xmin, ymin), font, 0.4, (255, 255, 255), 1, cv2.LINE_AA)
  cv2.imwrite(dirname+ '//' + name, img)
  cv2.imshow('temp', img)
  idx += 1
  cv2.waitKey(1)
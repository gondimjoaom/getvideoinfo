import cv2
import numpy as np
import os
from imutils.object_detection import non_max_suppression
import argparse

TEXT_TOP = 0
TEXT_BOTTOM = 96
TEXT_LEFT = 32
TEXT_RIGHT = 448

TEXT_TOP_NEW = 0
TEXT_BOTTOM_NEW = 0

layerNames = [
    "feature_fusion/Conv_7/Sigmoid",
    "feature_fusion/concat_3"]

ap = argparse.ArgumentParser()
ap.add_argument("-east", "--east", type=str, default='frozen_east_text_detection.pb')
ap.add_argument("-c", "--min-confidence", type=float, default=0.5)
args = vars(ap.parse_args())

darkrgb = (45, 45, 45)

def find_text(file):
    vidcap = cv2.VideoCapture(file)
    success, image = vidcap.read()
    cropped = image[TEXT_TOP:TEXT_BOTTOM, TEXT_LEFT:TEXT_RIGHT]
    ap.add_argument("-i", "--image", type=str, default=cropped)
    (H, W) = cropped.shape[:2]
    net = cv2.dnn.readNet(args["east"])
    blob = cv2.dnn.blobFromImage(cropped, 1.0, (W, H), (123.68, 116.78, 103.94), swapRB=True, crop=False)
    net.setInput(blob)
    (scores, geometry) = net.forward(layerNames)
    (numRows, numCols) = scores.shape[2:4]
    rects = []
    confidences = []
    for y in range(0, numRows):
        scoresData = scores[0, 0, y]
        xData0 = geometry[0, 0, y]
        xData1 = geometry[0, 1, y]
        xData2 = geometry[0, 2, y]
        xData3 = geometry[0, 3, y]
        anglesData = geometry[0, 4, y]
        for x in range(0, numCols):
            if scoresData[x] < args["min_confidence"]:
                continue
            (offsetX, offsetY) = (x * 4.0, y * 4.0)
            angle = anglesData[x]
            cos = np.cos(angle)
            sin = np.sin(angle)
            h = xData0[x] + xData2[x]
            w = xData1[x] + xData3[x]
            endX = int(offsetX + (cos * xData1[x]) + (sin * xData2[x]))
            endY = int(offsetY - (sin * xData1[x]) + (cos * xData2[x]))
            startX = int(endX - w)
            startY = int(endY - h)
            rects.append((startX, startY, endX, endY))
            confidences.append(scoresData[x])
    global TEXT_BOTTOM_NEW
    global TEXT_TOP_NEW
    boxes = non_max_suppression(np.array(rects), probs=confidences)
    for (startX, startY, endX, endY) in boxes:
        TEXT_TOP_NEW = startY
        TEXT_BOTTOM_NEW = endY + 5

def get_video_frames(file, framerate):
    filenamestart = file.find('ch')
    filenameend = file.find('.mp4')
    filename = file[filenamestart:filenameend]
    if not os.path.exists('frames/' + filename):
        os.makedirs('frames/' + filename)
    find_text(file)
    vidcap = cv2.VideoCapture(file)
    videolength = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    success, image = vidcap.read()
    count = 0
    while count < framerate:  # get first 30 frames
        cropped = image[TEXT_TOP_NEW:TEXT_BOTTOM_NEW, TEXT_LEFT:TEXT_RIGHT - 20]
        cv2.imwrite("frames/" + filename + "/frameBegin%d.jpg" % count, final_image)
        success, image = vidcap.read()
        count += 1
    count = framerate
    while count > 0:
        vidcap.set(1, videolength - count)
        success, image = vidcap.read()
        cropped = image[TEXT_TOP_NEW:TEXT_BOTTOM_NEW, TEXT_LEFT:TEXT_RIGHT - 20]
        cv2.imwrite("frames/" + filename + "/frameEnd%d.jpg" % (framerate - count), cropped)
        count -= 1

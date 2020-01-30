import pytesseract
from PIL import Image
import glob
import os
import json
import joblib
from sklearn import datasets
from skimage.feature import hog
from sklearn.svm import LinearSVC
import numpy as np

'''dataset = datasets.load_digits()
features = np.array(dataset.data, 'int16')
labels = np.array(dataset.data, 'int')

list_hog_fd = []
for feature in features:
    fd = hog(feature.reshape((64, 64)), orientations=9, pixels_per_cell=(14, 14), cells_per_block=(1, 1), visualise=False)
    list_hog_fd.append(fd)
hog_features = np.array(list_hog_fd, 'float64')

clf = LinearSVC()
clf.fit(hog_features, labels)
joblib.dump(clf, "digits_cls.pkl", compress=3)
clf = joblib.load("digits_cls.pkl")'''

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def get_video_begin_end(video, framerate):
    filenamestart = video.find('ch')
    filenameend = video.find('mp4')
    path_to_file = 'frames/' + video[filenamestart:filenameend - 1]
    framecount = framerate
    for i in sorted(glob.glob(path_to_file + '/frameBegin*.jpg'), key=os.path.getmtime):
        text = pytesseract.image_to_string(Image.open(i), lang='perfect')
        if 'frameBegin0.jpg' in i:
            date_begin = text[text.find('-') - 2 : text.find('-') + 8]
            begin_time = text[text.find(':') - 2 : text.find(':') + 6]
        if text[text.find(':') - 2 : text.find(':') + 6] != begin_time:
            begin_time = text[text.find(':') - 2: text.find(':') + 6]
            miliseconds_begin = 0.125 * framecount
            framecount = 8
        else:
            miliseconds_begin = 0.000
            framecount -= 1
    framecount = 0
    for i in sorted(glob.glob(path_to_file + '/frameEnd*.jpg'), key=os.path.getmtime):
        text = pytesseract.image_to_string(Image.open(i), lang='perfect')
        if 'frameEnd0.jpg' in i:
            date_end = text[text.find('-') - 2: text.find('-') + 8]
            end_time = text[text.find(':') - 2: text.find(':') + 6]
        if text[text.find(':') - 2: text.find(':') + 6] != end_time:
            end_time = text[text.find(':') - 2: text.find(':') + 6]
            framecount = 0
        framecount += 1
        #print(text)
    miliseconds_end = framecount * 0.125
    videofile = {
        'dateBegin': date_begin,
        'dateEnd': date_end,
        'timeBegin': begin_time + str(miliseconds_begin)[1:5],
        'timeEnd': end_time + str(miliseconds_end)[1:5]
    }

    with open(path_to_file + '/' + video[filenamestart:filenameend - 1] + '.json', 'w') as outfile:
        json.dump(videofile, outfile)
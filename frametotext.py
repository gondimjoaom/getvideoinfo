import pytesseract
from PIL import Image
import glob
import os
import json

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def get_video_begin_end(video, framerate):
    filenamestart = video.find('ch')
    filenameend = video.find('mp4')
    path_to_file = 'frames/' + video[filenamestart:filenameend - 1]
    framecount = framerate
    for i in sorted(glob.glob(path_to_file + '/frameBegin*.jpg'), key=os.path.getmtime):
        text = pytesseract.image_to_string(Image.open(i), lang='ENG')
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
        text = pytesseract.image_to_string(Image.open(i), lang='ENG')
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
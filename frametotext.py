import pyocr
import pyocr.builders
import pytesseract
import glob

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

for i in glob.glob('frames/*.jpg'):
    text = pytesseract.image_to_string(i, lang=None)
    print(text)
import pytesseract
from PIL import Image


pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

img = Image.open("storage/test.jpg") 
text = pytesseract.image_to_string(
    img,
    lang="ara+fra+eng",
    config="--psm 6")

print(text)

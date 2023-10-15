from PIL import Image
from pytesseract import pytesseract

image = Image.open('text.png')
image = image.resize((400,200))
text = pytesseract.image_to_string(image)
print(text)
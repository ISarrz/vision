import easyocr


reader = easyocr.Reader(['en','ru'], gpu = True)
bounds = reader.readtext('signs.png')


print(bounds)
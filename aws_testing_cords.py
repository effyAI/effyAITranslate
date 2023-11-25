import json
from pdf2image import convert_from_path 
from PIL import Image
import os
import shutil
from googletrans import Translator
from tqdm import tqdm
from threading import Thread

with open("test.json", "r") as f:
    data = json.load(f)

cords = []
page_dct = {}
blocks = data['Blocks']
pdf_name = "aws_axis_1_en.pdf"
pages = convert_from_path(pdf_name, 500)
for i,page in enumerate(pages):
    payload = {"page_number": i,
               "size": {"width": page.size[0],
                        "height": page.size[1]}}
    page_dct[i] = payload
print(page_dct)

translator_obj = Translator()


for b in tqdm(blocks[:10]):
    if b['BlockType'] == "LINE":
        payload = {"text": b['Text'],
                   "bbox": b['Geometry']['BoundingBox'],
                   "page": b['Page']}
        
        # translated Hindi, Bengali, Tamil, Telugu, Marathi, Gujarati, Kannada, Malayalam,
        payload["hindi"] = translator_obj.translate(payload['text'], dest='hi').text
        payload["bengali"] = translator_obj.translate(payload['text'], dest='bn').text
        payload["tamil"] = translator_obj.translate(payload['text'], dest='ta').text
        payload["telugu"] = translator_obj.translate(payload['text'], dest='te').text
        payload["marathi"] = translator_obj.translate(payload['text'], dest='mr').text
        payload["gujarati"] = translator_obj.translate(payload['text'], dest='gu').text
        payload["kannada"] = translator_obj.translate(payload['text'], dest='kn').text
        payload["malayalam"] = translator_obj.translate(payload['text'], dest='ml').text
        cords.append(payload)

"""
payload = {"text": "Hello",
              "bbox": {"Width": 0.1,
                      "Height": 0.1,
                      "Left": 0.1,
                      "Top": 0.1}}
"""

with open("translated2_pdf.json", "w") as f:
    f.write(str(cords))

result = "res"
if os.path.exists(result):
    shutil.rmtree(result)
if not os.path.exists(result):
    os.makedirs(result)


chng_pdf_png = {}
for i,cord in enumerate(cords[:10]):
    page_details = page_dct[cord['page']-1]
    page = pages[page_details['page_number']]

    width, height = page_details['size']['width'], page_details['size']['height']
    bbox = cord['bbox']
    x = int(bbox['Left'] * width)
    y = int(bbox['Top'] * height)
    w = int(x + bbox['Width']*width)
    h = int(y + bbox['Height']*height)
    # print(x, y, w, h)
    cropped = page.crop((x, y, w, h))

    cropped.save("res/{}.png".format(i))


import fitz
import json
import os
from unidecode import unidecode
from googletrans import Translator
my_pdf = "axis_og_pdfs/axis_1_en.pdf"
doc = fitz.open(my_pdf)
my_translator = Translator()

##removing the text from the pdf


blocks = {}
for page in doc:
    text_block = page.get_text("dict", flags=11)["blocks"]
    
    for b in text_block:
        
        font = b["lines"][0]["spans"][0]["font"]
        size = b["lines"][0]["spans"][0]["size"]
        color = b["lines"][0]["spans"][0]["color"]
        text = b["lines"][0]["spans"][0]["text"]
        print(b["lines"][0]["spans"][0]['origin'])
        rect = fitz.Point(b["lines"][0]["spans"][0]['origin'])
        if b['type'] == 0: 
            page.add_redact_annot(rect)
            page.apply_redactions()
        trans_text = my_translator.translate(text, dest='hi').text

        print("font: ", font)
        print("size: ", size)
        print("color: ", color)
        print("text: ", text)
        print("rect: ", rect)
        print("T-Text:", trans_text)

        page.insert_text(rect,  # bottom-left of 1st char
                     [trans_text],  # the text (honors '\n')
                     fontfile = "/home/infinity/Desktop/Effy_Internship/OCR _test/fonts/Tiro_Devanagari_Hindi/TiroDevanagariHindi-Regular.ttf",  # the default font
                     fontsize = size,  # the default font size
                     rotate = 0,  # also available: 90, 180, 270
                     encoding=fitz.TEXT_ENCODING_GREEK
                     )

        break
#         if b[6] == 0: #text
#             x0, y0, x1, y1 = b[:4]


#             text = unidecode(b[4])
#             rect = fitz.Point(x0, y0)
#             page.insert_text(rect, 
#                              )


doc.save("output.pdf")


# import fitz
# doc = fitz.open('/home/infinity/Desktop/Effy_Internship/OCR _test/axis_1_en.pdf') #"  # new or existing PDF
# page = doc[0]  # new or existing page via doc[n]
# p = fitz.Point(20.152299880981445, 392.17340087890625)  # start point of 1st line
# print(p)
# text = "sdwwc"
# # the same result is achievable by
# # text = ["Some text", "spread across", "several lines."]

# rc = page.insert_text(p,  # bottom-left of 1st char
#                      text,  # the text (honors '\n')
#                      fontname = "helv",  # the default font
#                      fontsize = 11,  # the default font size
#                      rotate = 0,  # also available: 90, 180, 270
#                      )
# print("%i lines printed on page %i." % (rc, page.number))

# doc.save("text.pdf")
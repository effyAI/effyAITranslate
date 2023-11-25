import fitz  # PyMuPDF
from googletrans import Translator

# Open the PDF
doc = fitz.open('axis_og_pdfs/axis_en_curve_text.pdf')

# Initialize a translator
translator = Translator()

# Iterate over PDF pages
for page_num in range(len(doc)):
    page = doc[page_num]
    # Get text blocks
    text_blocks = page.get_text("dict")["blocks"]
    with open('test_text_block.txt', 'w') as f:
        f.write(str(text_blocks))
    for block in text_blocks:
        # Check if the block is a text block
        if block['type'] == 0:  # 0 is the type for text blocks
            # For each text block, translate the text and replace the original text
            for line in block["lines"]:
                for span in line["spans"]:
                    r = fitz.Rect(span["bbox"])
                    page.add_redact_annot(r)
    page.apply_redactions()
    # doc.save('temp_axis_es_reduct.pdf')
    
    for block in text_blocks:
        # Check if the block is a text block
        if block['type'] == 0:  # 0 is the type for text blocks
            # For each text block, translate the text and replace the original text
            for line in block["lines"]:
                for span in line["spans"]:
                    r = fitz.Rect(span["bbox"])
                    page.add_redact_annot(r)
                    # page.apply_redactions()
    # break
doc.save('temp_axis_es_bbox.pdf')

# for page_num in range(len(doc)):
#     page = doc[page_num]
#     # Get text blocks
#     text_blocks = page.get_text("dict")["blocks"]
#     with open('test_text_block.txt', 'w') as f:
#         f.write(str(text_blocks))
#     for block in text_blocks:
#         # Check if the block is a text block
#         if block['type'] == 0:  # 0 is the type for text blocks
#             # For each text block, translate the text and replace the original text
#             for line in block["lines"]:
#                 for span in line["spans"]:
#                     r = fitz.Rect(span["bbox"])
#                     page.add_redact_annot(r)
#                     page.apply_redactions()
            

#                 for span in line["spans"]:
#                     original_text = span['text']
#                     translation = translator.translate(original_text, dest='es')  # Translate to Spanish
#                     r = fitz.Point(span['origin'])
                    

#                     page.insert_text(point=r, 
#                                      text=translation.text,
#                                      fontfile=f"/home/infinity/Desktop/Effy_Internship/OCR _test/fonts/Lato/{span['font']}.ttf",
#                                      fontsize=span['size'],)

#     break                    

# # Save the PDF
# doc.save('temp_axis_es.pdf')

import fitz  # PyMuPDF
from googletrans import Translator
import json
import io
import os


def make_pdf(fileptr, text, rect, font="sans-serif", archive=None):
    """Make a memory DocumentWriter from HTML text and a rect.

    Args:
        fileptr: a Python file object. For example an io.BytesIO().
        text: the text to output (HTML format)
        rect: the target rectangle. Will use its width / height as mediabox
        font: (str) font family name, default sans-serif
        archive: fitz.Archive parameter. To be used if e.g. images or special
                fonts should be used.
    Returns:
        The matrix to convert page rectangles of the created PDF back
        to rectangle coordinates in the parameter "rect".
        Normal use will expect to fit all the text in the given rect.
        However, if an overflow occurs, this function will output multiple
        pages, and the caller may decide to either accept or retry with
        changed parameters.
    """
    # use input rectangle as the page dimension
    mediabox = fitz.Rect(0, 0, rect.width, rect.height)
    # this matrix converts mediabox back to input rect
    matrix = mediabox.torect(rect)

    story = fitz.Story(text, archive=archive)
    body = story.body
    body.set_properties(font=font)
    writer = fitz.DocumentWriter(fileptr)
    while True:
        device = writer.begin_page(mediabox)
        more, _ = story.place(mediabox)
        story.draw(device)
        writer.end_page()
        if not more:
            break
    writer.close()
    return matrix

# Open the PDF
doc = fitz.open('axis_og_pdfs/axis_1_en.pdf')

# Initialize a translator
translator = Translator()

# Iterate over PDF pages
bbox = []
for page_num in range(len(doc)):
    page = doc[page_num]
    # Get text blocks
    text_blocks = page.get_text("dict")["blocks"]
    # with open('test_text_block.txt', 'w') as f:
    #     f.write(str(text_blocks))
    for block in text_blocks:
        # Check if the block is a text block
        if block['type'] == 0:  # 0 is the type for text blocks
            # For each text block, translate the text and replace the original text
            for line in block["lines"]:
                for span in line["spans"]:
                    rect = fitz.Rect(span["bbox"])
                    bbox.append(rect)
                    page.add_redact_annot(rect)
                    page.apply_redactions()

                for span in line["spans"]:
                    
                    original_text = span['text']
                    print(original_text)
                    translation = translator.translate(original_text, dest='es')  # Translate to Spanish
                    point = fitz.Point(span['origin'])
                    colour = fitz.sRGB_to_pdf(span['color'])
                    
                    rect = fitz.Rect(span["bbox"])
                    
                    ins_text = translation.text

                    # fileptr = io.BytesIO()

                    # html = f'<p>{ins_text}</p>'

                    # matrix = make_pdf(fileptr, html, rect)

                    # src = fitz.open("pdf", fileptr)
                    # if src.page_count > 1:
                    #     print("Overflow")
                    
                    # page.show_pdf_page(rect, src, 0)
                    
                    # story = fitz.Story(html=html)
                    # more, _ = story.place(rect)
                    # story.draw(page)

                    ##meth 1
                    # # font = fitz.Font(fontfile=f"/home/infinity/Desktop/Effy_Internship/OCR _test/fonts/Lato/{span['font']}.ttf")
                    # tw = fitz.TextWriter(rect)
                    # tw.append(pos=point,text=ins_text, fontsize=int(span['size']))

                    # tw.write_text(page, color=fitz.sRGB_to_pdf(span['color']))

                    # print(ins_text)
                    # print(translation.text.encode('utf-8'))

                    # #meth 2
                    # page.write_text(point=r,
                    #                 text=ins_text,
                    #                 fontname="notos",
                    #                 # fontfile=f"/home/infinity/Desktop/Effy_Internship/OCR _test/fonts/Lato/{span['font']}.ttf",
                    #                 fontsize=span['size'],
                    #                 color=fitz.sRGB_to_pdf(span['color']))

                    #meth 3
                    rc = page.insert_text(point=point, 
                                     text=ins_text,
                                     fontname="notos",
                                    #  fontfile=f"/home/infinity/Desktop/Effy_Internship/OCR _test/fonts/Lato/{span['font']}.ttf",
                                     fontsize=span['size'],
                                     color=fitz.sRGB_to_pdf(span['color']),
                                     encoding=fitz.TEXT_ENCODING_CYRILLIC)
                    print(rc)
    break                    

# Save the PDF
print(bbox)
doc.save('temp_axis_es.pdf')
import fitz  # PyMuPDF

# Open the PDF
doc = fitz.open('axis_og_pdfs/axis_1_en.pdf')

# Iterate over PDF pages
for page_num in range(len(doc)):
    page = doc[page_num]
    # Get text blocks
    text_blocks = page.get_text("dict")["blocks"]
    for block in text_blocks:
        # Check if the block is a text block
        if block['type'] == 0:  # 0 is the type for text blocks
            # For each text block, redact the area of the block
            for line in block["lines"]:
                for span in line["spans"]:
                    r = fitz.Rect(span["bbox"])
                    page.add_redact_annot(r)

    # Apply redactions (remove text)
    page.apply_redactions()

# Save the PDF
doc.save('output.pdf')
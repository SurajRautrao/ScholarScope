import fitz  # PyMuPDF

def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""

    for page in doc:
        text += page.get_text()

    # CLEAN TEXT
    text = text.replace("\n", " ")
    text = " ".join(text.split())  # remove extra spaces

    return text

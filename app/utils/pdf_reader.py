import re

import fitz  # PyMuPDF

# a line that is only a references heading, e.g. "References", "7 REFERENCES", "Bibliography"
REFERENCES_HEADING = re.compile(r"^\s*(\d+\.?\s*)?(references|bibliography)\s*$", re.IGNORECASE)


def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""

    for page in doc:
        text += page.get_text()

    text = strip_references(text)

    # CLEAN TEXT
    text = text.replace("\n", " ")
    text = " ".join(text.split())  # remove extra spaces

    return text


def strip_references(text):
    """Cut the text at the references heading, dropping the citation list
    (and any appendix after it) so other papers' titles aren't analyzed as this one's."""
    lines = text.split("\n")

    headings = [i for i, line in enumerate(lines) if REFERENCES_HEADING.match(line)]

    # only trust a heading past the first third of the paper (not a table of contents)
    if headings and headings[-1] > len(lines) / 3:
        return "\n".join(lines[:headings[-1]])

    return text

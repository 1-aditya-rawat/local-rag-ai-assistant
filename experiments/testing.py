from pdf_reader import extract_text_from_pdf

with open("MLtesting.pdf", "rb") as f:
    text = extract_text_from_pdf(f)

print(text[:2000])  
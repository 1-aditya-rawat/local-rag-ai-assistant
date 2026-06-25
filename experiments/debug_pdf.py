# 1.Debugging Text Extraction

# from pdf_reader import extract_text_from_pdf

# with open("pythonTesting.pdf", "rb") as f:
#     text = extract_text_from_pdf(f)

# print("f-string" in text.lower())
# print("f strings" in text.lower())
# print("fstrings" in text.lower())

# 2.Debugging Chunking

# from pdf_reader import extract_text_from_pdf
# from utils import chunk_text

# with open(r"C:\Users\Aditya Rawat\Desktop\rag_app\pythonTesting.pdf", "rb") as f:
#     text = extract_text_from_pdf(f)

# chunks = chunk_text(text)

# found = 0

# for i, chunk in enumerate(chunks):

#     if "f-string" in chunk.lower():

#         found += 1

#         print(f"\nFOUND IN CHUNK {i}")
#         print(chunk[:1000])

# print("\nTotal Chunks Containing f-string:", found)

# Checking which data doesn't have metadata

from database import collection

data = collection.get()

for i, meta in enumerate(data["metadatas"]):
    if meta is None:
        print(i)
    
# Two ways of extracting content from pdf files from Python. 
# 1. Using pypdf library. 
# 2. Using PyMuPDF library (Retuns the content in the better manner + supports multiple formats too)
from pypdf import PdfReader 
reader = PdfReader("demo.pdf")

# Return the number of pages in the pdf file.
print(len(reader.pages))

# Give you access to the first page in the pdf file.
page = reader.pages[0]
# print(page);

# Extracts the content from the first page of the pdf file.
retrieve_text = page.extract_text()
print(retrieve_text)


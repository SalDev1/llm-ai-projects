
# Import libs such as PyMuPDF & fitz
import fitz 
# Returns the array of pages from the pdf and open the pdf document.
doc  = fitz.open("demo.pdf")
print(type(doc))  # <class 'fitz.fitz.Document'>

print(doc.page_count)  # Number of pages in the pdf file.

main_txt = "";
for page in doc : 
    text = page.get_text()
    main_txt += text

print(main_txt)
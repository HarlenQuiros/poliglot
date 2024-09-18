from PyPDF2 import PdfReader

def read_pdf(file_path):
    reader = PdfReader(file_path)
    for page in reader.pages:
        text = page.extract_text()
        print(text)

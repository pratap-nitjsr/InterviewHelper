import PyPDF2

def read_file(file_ptr):
    information = ""
    pdf = PyPDF2.PdfReader(file_ptr)
    for i in pdf.pages:
        page_content = i.extract_text()
        information+= page_content
    return information
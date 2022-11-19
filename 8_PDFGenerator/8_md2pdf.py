import os
from md2pdf.core import md2pdf

notesRoot = "C:/Users/jazzm/Desktop/DocVoorSchool/Notes"
notesDestination = "C:/Users/jazzm/Desktop/DocVoorSchool/3-Python OOP/PythonLabo/8_PDFGenerator/Converted_pdf"
for root, dirs, files in os.walk(notesRoot):
    for file in files:
        if file.endswith(".md"):
            pdfFilePath = os.path.join(root, file)
            subdir = root.replace(notesRoot, "")
            destinationPath = os.path.join(notesDestination + subdir, file)
            md2pdf(pdfFilePath,
                md_content=None,
                md_file_path=destinationPath,
                css_file_path=None,
                base_url=None)
            print(destinationPath)




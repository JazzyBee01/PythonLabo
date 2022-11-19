import aspose.words as aw
import os

notesRoot = "C:/Users/jazzm/Desktop/DocVoorSchool/Notes"
notesDestination = "C:/Users/jazzm/Desktop/DocVoorSchool/3-Python OOP/PythonLabo/8_PDFGenerator/Converted_pdf"
for root, dirs, files in os.walk(notesRoot):
    for file in files:
        if file.endswith(".md"):
            filePath = os.path.join(root, file)
            doc = aw.Document(filePath)
            subdir = root.replace(notesRoot, "")
            destinationPath = os.path.join(notesDestination + subdir, file)
            doc.save(destinationPath[:-2]+"pdf") #strip .md of end
            print(destinationPath)




import PyPDF2


class Reader():
    def __init__(self, charLimit=500):
        self.charLimit = charLimit

    def parse(self, filePath):
        try:
            fileContent = ""
            with open(filePath, "rb") as fh:
                myReader = PyPDF2.PdfReader(fh)
                pageCount = len(myReader.pages)
                for i in range(10):
                    fileContent += myReader.pages[i].extract_text()
                if len(fileContent) > self.charLimit:
                    fileContent = fileContent[:self.charLimit]
            return fileContent
        except Exception:
            return None

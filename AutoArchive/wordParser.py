import textract


class Reader():
    def __init__(self, charLimit=500):
        self.charLimit = charLimit

    def parse(self, filePath):
        try:
            fileContent = textract.process(filePath).decode('UTF-8')
            if len(fileContent) > self.charLimit:
                fileContent = fileContent[:self.charLimit]
            return fileContent
        except Exception:
            return None

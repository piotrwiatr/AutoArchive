class Reader():
    def __init__(self, charLimit=300):
        self.charLimit = charLimit

    def parse(self, filePath):
        try:
            fileContent = ""
            with open(filePath, "r") as fh:
                fileContent = repr(fh.read())
                if len(fileContent) > self.charLimit:
                    fileContent = fileContent[:self.charLimit]
            return fileContent
        except Exception:
            return None

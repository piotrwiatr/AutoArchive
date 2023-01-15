from PIL import Image
import pytesseract
import numpy as np


class NotEnoughImgText(Exception):
    pass


class Reader():
    def __init__(self, charLowerBound=25, charLimit=500):
        self.charLowerBound = charLowerBound
        self.charLimit = charLimit

    def parse(self, filePath):
        try:
            img = np.array(Image.open(filePath))
            fileContent = pytesseract.image_to_string(img).replace("\n", "")
            if len(fileContent) > self.charLimit:
                fileContent = fileContent[:self.charLimit]

            if len(fileContent) < self.charLowerBound:
                raise NotEnoughImgText
            return fileContent
        except Exception:
            return None

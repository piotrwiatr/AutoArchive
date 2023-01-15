import chatgpt
import plaintext
import pdfparser
import wordParser
import powerpoint
import imagerecog


class FileExtensionNotSupported(Exception):
    pass

# Get filepaths
# Get out directories


class FileParser():
    def __init__(self):
        '''
        FileParser object that, given a filepath, determines its file extension, reads the contents of the file, and sets a request to
        chatGPT and returns the response
        '''
        self.formats = ["txt", "md", "html",
                        "htm", "xml", "csv", "json", "yaml", "pdf", "py", "docx", "pptx", "png", "jpeg", "jpg", "gif"]
        self.textFormats = ["txt", "md", "html", "htm",
                            "xml", "json", "csv", "json", "yaml", "py"]
        self.imageFormats = ["png", "jpeg", "jpg", "gif"]

    # finds the extension of the file and ensures that it is supported.
    def checkFileExtension(self, fileName):
        for extension in self.formats:
            if fileName.lower().endswith(extension):
                return extension
        raise FileExtensionNotSupported

    # function that takes a given filepath and returns a certain portion of its content
    def getFileContent(self, filePath):
        path = self.sanitizeFilePath(filePath)

        try:
            extension = self.checkFileExtension(path)
        except Exception:
            raise FileExtensionNotSupported
        else:
            reader = None
            if extension in self.textFormats:
                reader = plaintext.Reader()
            elif extension in self.imageFormats:
                reader = imagerecog.Reader()
            elif extension == "pdf":
                reader = pdfparser.Reader()
            elif extension == "docx":
                reader = wordParser.Reader()
            elif extension == "pptx":
                reader = powerpoint.Reader()

            if reader != None:
                content = reader.parse(path)
                return (content, extension)

    # santizies output by removing all backslashes and replacing them with forward slashes

    def sanitizeFilePath(self, filePath):
        rFilePath = filePath
        rFilePath = rFilePath.replace("\\", "/")
        rFilePath = rFilePath.replace("\\\\", "//")
        return rFilePath

    # sends request to chatgpt and returns a dictionary mapping the original file to its modifications
    def parseFile(self, filePath, outputDirs):
        path = self.sanitizeFilePath(filePath)
        try:
            content, extension = self.getFileContent(path)
        except Exception:
            return None
        if content == None:
            return None

        # gets response from chatGPT
        gpt = chatgpt.ChatGPT()
        response = None
        try:
            response = gpt.request(outputDirs, content)
        except Exception:
            return None

        # checks if the location ends with an ending slash or not to check if chatgpt returns a valid location
        response['fileName'] = response['fileName'] + '.' + extension
        if not response['location'].endswith('/'):
            if response['location'] in outputDirs:
                return {path: {"path": response['location'], "name": response['fileName'], "confidence": (not response["unsure"])}}
            elif response['location'] + '/' in outputDirs:
                return {path: {"path": response['location'] + '/', "name": response['fileName'], "confidence": (not response["unsure"])}}
        else:
            if response['location'] in outputDirs:
                return {path: {"path": response['location'], "name": response['fileName'], "confidence": (not response["unsure"])}}
            elif response['location'][-1] in outputDirs:
                return {path: {"path": response['location'][-1], "name": response['fileName'], "confidence": (not response["unsure"])}}
        return None

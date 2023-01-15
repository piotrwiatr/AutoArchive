import openai
import json
import string
# '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'


class GPTError(Exception):
    pass


class ChatGPT():
    def __init__(self, apiKey='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', keys=["fileName", "location", "unsure"]):
        '''
        chatGPT file rename/relocate module
        arguments:

        0: apiKey (in order to use openAI API) (String)
        1: list of keys that chatGPT should include in its json (optional) (list of strings)
        '''
        openai.api_key = apiKey
        self.keys = keys

    def request(self, listOfDirNames, fileContent, retries=0):
        '''
        Module that takes a list of dir names and file content and asks chatGPT what it should be renamed/relocated to

        arguments:
        0: listOfDirNames (list of Strings)
        1: fileContent (string)
        '''

        # if chatGPT fails to give a statisfatory response, raise error
        if retries > 2:
            raise GPTError

        # Send request to ChatGPT
        # prompt
        requestNameDirChange = "A file contains the following text: \'" + fileContent + "\'. The following folders are available: " + \
            (','.join(listOfDirNames)) + \
            ". Based on the parsed information and the folders provided what should I name this file and which folder should I store it in? Your response should be only one line in the json format of {\"fileName\":\"file-name-here\", \"location\":\"Folder_Name_Here\", \"unsure\":False} Where \"fileName\" is a document named separates by \"dashes\" in lowercase, location is an absolute path written with forward slashes, and \"unsure\" indicates if you think your answer is illogical. You are not allowed to answer except in the provided json format."

        # ChatGPT request using the customized prompt
        response = openai.Completion.create(
            model="text-davinci-003", prompt=requestNameDirChange, temperature=0, max_tokens=2048)

        # Extracting Text
        response = response["choices"][0]['text']

        # Finds beginning and end curly brace of the json output
        # removes extraneous info, such as newline characters
        firstIndex = -1
        secondIndex = -1
        foundFirstIndex = False
        foundSecondIndex = False
        for i in range(len(response)):
            if response[i] == "{" and not foundFirstIndex:
                firstIndex = i
                foundFirstIndex = True
            if response[len(response) - 1 - i] == "}" and not foundSecondIndex:
                secondIndex = (len(response) - 1) - i
                foundSecondIndex = True

        # if no opening/ending curly brace was found
        if firstIndex < 0 or secondIndex < 0:
            retries += 1
            return self.request(listOfDirNames, fileContent, retries)

        # santizie the output to make it valid json
        response = response[firstIndex: secondIndex+1]
        response = response.replace("True", "true")
        response = response.replace("False", "false")

        # if unable to load Json, resend request to chatGPT
        try:
            responseJson = json.loads(response)
        except Exception:
            retries += 1
            return self.request(listOfDirNames, fileContent, retries)

        # list of keys:
        listOfJsonKeys = responseJson.keys()

        # checks if all the desired keys are in the responseJson
        for key in self.keys:
            if key not in listOfJsonKeys:
                retries += 1
                return self.request(listOfDirNames, fileContent, retries)

        # remove spaces, file extensions, periods (extensions) from any of the values.
        # we want to keep the - and _ characters
        punc = string.punctuation.replace("-", "").replace("_", "")
        jsonValue = responseJson["fileName"]
        try:
            endIndex = jsonValue.index(".")
        except Exception:
            endIndex = len(jsonValue)

        newValue = jsonValue[:endIndex]
        newValue = newValue.lower()

        for chars in punc:
            newValue.replace(chars, "")
        newValue = newValue.replace(" ", "-")
        newValue = newValue.replace("_", "-")

        responseJson["fileName"] = newValue

        return responseJson


#thing = ChatGPT()

# dirNames = ['C://Users/Documents', 'C://Users/Downloads',
#            'C://Users/Documents/Math', 'C://Users/Documents/English']
#content = "According to the fundamnetal theorem of calculus, the area under a curve with respect to two endpoints can be written as the anti-derivative evalued at the left endpoint minus the anti-derivative evaluated at the right endpoint"
#print(thing.request(dirNames, content))

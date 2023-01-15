import os
import fileParser

# needs to get input file done
# parseFile and get input from chatgpt done
# function for renaming the file done
# function for moving the file
# function for renaming + moving the file
# function that automatically creates a file that keeps track of changes


class Processor():
    def __init__(self):
        pass

    def __novelFileName(self, path):
        if os.path.isfile(path):

            justName = ''
            ext = ''
            i = 0
            while path[i] != '.':
                justName += path[i]
                i += 1

            ext = path[i:]

            i = 1
            while os.path.isfile(justName + str(i) + ext):
                i += 1

            return justName + str(i) + ext

        return path

    def __safeRename(self, path, newPath):
        safePath = self.__novelFileName(newPath)
        os.rename(path, safePath)

    def parse(self, filePath, outputDirs):
        myParser = fileParser.FileParser()
        return myParser.parseFile(filePath, outputDirs)

    def getCleanPath(self, filePath):
        myParser = fileParser.FileParser()
        cleanPath = myParser.sanitizeFilePath(filePath)
        return cleanPath

    def getPathOnly(self, filePath):
        cleanPath = self.getCleanPath(filePath)
        endIndex = len(cleanPath)
        for i in range(len(cleanPath)):
            if cleanPath[len(cleanPath) - 1 - i] == "/" or cleanPath[len(cleanPath) - 1 - i] == "\\":
                endIndex = len(cleanPath) - 1 - i
                break

        return cleanPath[:endIndex+1]  # includes final slash

    def getNameOnly(self, filePath):
        cleanPath = self.getCleanPath(filePath)
        pathOnly = len(self.getPathOnly(cleanPath)) - 1
        return filePath[pathOnly:]

    def renameFile(self, filePath, suggestions):
        cleanPath = self.getCleanPath(filePath)
        if suggestions == None:
            return None
        locationToFile = self.getPathOnly(cleanPath)
        newName = locationToFile + suggestions[cleanPath]["name"]
        self.__safeRename(cleanPath, newName)

        return {cleanPath: newName}

    def moveFile(self, filePath, suggestions):
        cleanPath = self.getCleanPath(filePath)

        if suggestions == None:
            return None

        name = self.getNameOnly(cleanPath)
        newLocation = suggestions[cleanPath]["path"] + name
        self.__safeRename(cleanPath, newLocation)
        return {cleanPath: newLocation}

    def moveRenameFile(self, filePath, suggestions):
        cleanPath = self.getCleanPath(filePath)

        if suggestions == None:
            return None

        if suggestions[cleanPath]["path"].endswith("/"):
            newFile = suggestions[cleanPath]["path"] + \
                suggestions[cleanPath]["name"]
        else:
            newFile = suggestions[cleanPath]["path"] + "/" + \
                suggestions[cleanPath]["name"]

        self.__safeRename(cleanPath, newFile)
        return {cleanPath: newFile}

    # Print iterations progress
    def printProgressBar(self, iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
        percent = ("{0:." + str(decimals) + "f}").format(100 *
                                                         (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)
        # Print New Line on Complete
        if iteration == total:
            print()

    # files, verification level, renaming, moving
    # ignoreConfidence = 0(do everything from chatgpt), 1(confirm with user) 2(check with every file)

    def process(self, listOfFiles=[], listOfDirs=[], ignoreConfidence=0, renaming=True, moving=True, verbose=False, debug=None):
        if len(listOfFiles) == 0 or len(listOfDirs) == 0:
            return None

        crimesCommitted = []
        i = 0

        for file in listOfFiles:
            
            if verbose:
                self.printProgressBar(i, len(listOfFiles), "Progress: ", "Complete", length=25, printEnd=" - ")

            i += 1

            if verbose:
                print(f"Currently dealing with {file} ... ", end="")
                

            suggestion = self.parse(file, listOfDirs)
            if suggestion == None:
                if verbose:
                    print(
                        f"ChatGPT failed to return a reasonable response, skipping {file}")
                pass
            else:
                if verbose:
                    print(
                        "Validating response")
                
                if (suggestion[file]["confidence"] == False and ignoreConfidence == 1) or ignoreConfidence == 2:
                    morallyObligedToContinue = input(
                        f"ChatGPT suggests that {file} ought to be placed in {suggestion[file]['path']} as {suggestion[file]['name']}, should it continue (Y/N)? ").lower()
                    if morallyObligedToContinue == "n" or morallyObligedToContinue == "no":
                        pass

                change = None
                if renaming and moving:
                    change = self.moveRenameFile(file, suggestion)
                if renaming and not moving:
                    change = self.renameFile(file, suggestion)
                if not renaming and moving:
                    change = self.moveFile(file, suggestion)

                if change != None:
                    crimesCommitted.append(change)


        if debug:
            crimesCommitted = str(crimesCommitted)
            try:
                with open(debug + "changes.txt", "a+") as fh:
                    fh.write("\n" + crimesCommitted)
            except:
                with open(debug + "changes.txt", "w+") as fh:
                    fh.write("\n" + crimesCommitted)

        if verbose:
            self.printProgressBar(i, len(listOfFiles), "Progress: ", "Complete", length=25, printEnd=" - ")
            print("Process completed! >:)")


# dirNames = ['Documents', 'Downloads',
#             'CompSci']
# fileNames = ['letlslgls.pdf', 'test.html', 'test.json']
# myProcessor = Processor()
# myProcessor.process(fileNames, dirNames)
# suggestions = self.parse(filePath)


# Errors: No display for single file runs
# Errors: Cannot write a file if that file already exists

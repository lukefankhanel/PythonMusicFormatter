import sys
import os
import traceback
import json

def printErrorMessage(message, exit):
    print("ERROR: " + message + "\nExiting...")
    if exit:
        sys.exit()


class FileManager:
    def __init__(self, workingDirectory):
        self.foundMusicFile = False
        self.workingDirectory = workingDirectory

    def createOutputDirectories(self):
        if not self.foundMusicFile:
            directory_names = ["complete","partial","failure"]
            for name in directory_names:
                self.createDirectory(name)
            self.foundMusicFile = True

    def createDirectory(self, path):
        self.createOutputDirectories()
        try:
            os.makedirs(os.path.join(self.workingDirectory, path), exist_ok=True)
        except:
            printErrorMessage("Couldn't create desired directory \"" + path + "\"")

    def moveFile(self, target, destination):
        print("Moving File")
    

class JSONManager:
    def __init__(self, inputFileLocation, outputFileLocation):
        self.readInputJSONFile(inputFileLocation)
        self.outputFileLocation = outputFileLocation
        self.objectCollection = {
            "complete": [],
            "partial":[],
            "incomplete":[],
            "generic": []
        }

    def appendObject(self, object):
        try:
            # statusSummary = object["successStatus"]["summary"]
            # if statusSummary == "Complete":
            #     self.appendObjectToComlete(object)
            # elif statusSummary == "Partial":
            #     self.appendObjectToPartial(object)
            # elif statusSummary == "None Found - Incomplete":
            #     self.appendObjectToPartial(object)
            self.objectCollection[object["successStatus"]["summary"]].append(object)
        except:
            self.objectCollection["generic"].append(object)

    def getInputJSONDictionary(self):
        return self.InputJSON

    def readInputJSONFile(self, fileLocation):
        try:
            with open(fileLocation, encoding="utf-8") as JSONFile:
                self.InputJSON = json.load(JSONFile)
                self.InputJSON["artistNameTranslations"]
                fields = self.InputJSON["metadataFieldMatches"]
                foundValuesDictionary = {
                    "title": False,
                    "album": False,
                    "artist": False,
                    "date": False,
                    "delimiters": False
                }
                for key, value in fields.items():
                    if len(value) < 1:
                        raise KeyError
                    for checkKey, checkValue in foundValuesDictionary.items():
                        if checkKey == key:
                            foundValuesDictionary[checkKey] = True
                for key, value in foundValuesDictionary.items():
                    if value == False:
                        raise KeyError 
        except KeyError:
            printErrorMessage("Couldn't find required fields in loaded JSON file.", True) #TODO List out JSON format
        except FileNotFoundError:
            printErrorMessage("Couldn't read from supplied settings JSON file.", True)
        except json.JSONDecodeError:
            printErrorMessage("Couldn't read JSON from supplied settings file.", True)
        except:
            print(traceback.print_exc())
            printErrorMessage("An unknown error occurred while reading settings JSON file.", True)

    def outputJSONArray(self):
        with open(self.outputFileLocation, 'w', encoding="utf-8") as file:
            json.dump(self.objectCollection, file, indent=4, ensure_ascii=False)
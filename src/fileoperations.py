import json

def moveFile(target, destination):
    print("Moving File")


class JSONManager:
    def __init__(self, inputFileLocation, outputFileLocation):
        self.readInputJSONFile(inputFileLocation)
        self.outputFileLocation = outputFileLocation
        self.objectArray = []

    def appendObject(self, object):
        self.objectArray.append(object)

    def readInputJSONFile(self, fileLocation):
        with open(fileLocation, encoding="utf-8") as JSONFile:
            self.InputJSON = json.load(JSONFile)

    def getInputJSONDictionary(self):
        return self.InputJSON

    def outputJSONArray(self):
        with open(self.outputFileLocation, 'w', encoding="utf-8") as file:
            json.dump(self.JSONArray, file, indent=4, ensure_ascii=False)
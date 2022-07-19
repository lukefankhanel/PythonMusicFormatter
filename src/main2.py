import os
import argparse
import fileoperations
import audiotypes

def main():

    #TODO App and argument descriptions
    argumentParser = argparse.ArgumentParser(description="Optional app description")
 
    argumentParser.add_argument("--workingFolder", "-w", 
        type=str, 
        required=True,
        metavar="\b",
        help='A required integer positional argument')
    argumentParser.add_argument("--settingsFile", "-s", 
        type=str,
        required=True,
        metavar="\b",
        help='A required integer positional argument')
    argumentParser.add_argument("--logFileName", "-l", 
        type=str,
        required=True,
        metavar="\b",
        help='A required integer positional argument')

    arguments = argumentParser.parse_args()


    jm = fileoperations.JSONManager(arguments.settingsFile, os.path.join(arguments.workingFolder, arguments.logFileName))
    fm = fileoperations.FileManager(arguments.workingFolder)
    
    for (dirpath, dirnames, filenames) in os.walk(arguments.workingFolder):
        for filePath in filenames:
            file = audiotypes.createFileObject(os.path.join(dirpath, filePath), jm.getInputJSONDictionary())
            if file:
                file.findUpdateSongInformation()
                jm.appendObject(file.serializeToDictionary())
                

        break
    print("MADE IT HERE")
    jm.outputJSONArray()

if __name__ == "__main__":
    main()
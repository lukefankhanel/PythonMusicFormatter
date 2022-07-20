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
                print("Processing music file: " + file.getFileLocation())
                file.findUpdateSongInformation()
                print(file.applyNameTranslations())
                jm.appendObject(file.serializeToDictionary())
                print("Song processing complete, continuing...\n\n-----------------\n")
        break
    print("Finished processing songs, outputting JSON log file...")
    jm.outputJSONArray()

if __name__ == "__main__":
    main()
import json
from abc import ABC, abstractmethod
from mutagen.oggopus import OggOpus
from mutagen.mp4 import MP4

def createFileObject(fileLocation, findValuesJSON):
    pass


class SongFileJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, SongFile):
            return json.dumps({ "FileTitle": obj.getFileTitle() })
        return json.JSONEncoder.default(self, obj)

class SongFile(ABC):

    # functions:
    # pull data
    # update
    # does x field exist? 
    # export to JSON object with the fields we want

    def __init__(self, fileLocation): 
        self.fileLocation = fileLocation # string
        self.initializeFileFields()


        # videoUploader # string
        # videoUploadDate # string
        # videoTitle # string
        # videoDescription # string
        # videoURL # string (Not guarrentied)

        # foundSongTitle # string
        # foundSongArtist # string
        # foundSongAlbum # string
        # foundSongDate # string
        # foundSongComment # string

    def printFileMetadata(self):
        print(self.file.pprint())
    
    def serializeToDictionary(self):
        return { "FileTitle": self.getFileTitle() }

    @abstractmethod
    def initializeFileFields(self):
        pass

    def getFileTitle(self):
        return self.fileTitle



class OGGFile(SongFile):
    def __init__(self, fileLocation):
        self.file = OggOpus(fileLocation)
        super().__init__(fileLocation)

    def initializeFileFields(self):
        self.fileTitle = self.file["title"][0]
        self.fileUploader = self.file["artist"][0]
        self.fileUploadDate = self.file["date"][0]
        self.fileDescription = self.file["description"][0]
        self.fileURL = self.file["purl"][0]



class MP4File(SongFile):
    def __init__(self, fileLocation):
        self.file = MP4(fileLocation)
        super().__init__(fileLocation)

    def initializeFileFields(self):
        self.fileTitle = self.file["\xa9nam"][0]
        self.fileUploader = self.file["\xa9ART"][0]
        self.fileUploadDate = self.file["\xa9day"][0]
        self.fileDescription = self.file["desc"][0]
        self.fileURL = self.file["purl"][0] #NOT Assured, must catch all of them

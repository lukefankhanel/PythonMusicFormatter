from asyncio.windows_events import NULL
import json
from abc import ABC, abstractmethod
from mutagen.oggopus import OggOpus
from mutagen.mp4 import MP4

#TODO pull album from raw metadata

def createFileObject(fileLocation, JSONDictionary):
    if fileLocation.endswith(".opus"):
        return OGGFile(fileLocation, JSONDictionary)
    elif fileLocation.endswith(".m4a") or fileLocation.endswith(".mp4"):
        return MP4File(fileLocation, JSONDictionary)
    else:
        return None



class SongFile(ABC):
    def __init__(self, fileLocation, JSONDictionary):
        self.fileLocation = fileLocation # string
        self.metadataFieldMatches = JSONDictionary["metadataFieldMatches"]
        self.artistNameTranslations = JSONDictionary["artistNameTranslations"]
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
    @abstractmethod
    def initializeFileFields(self):
        pass

    @abstractmethod
    def setMetadataField(self, field, value):
        pass

    @abstractmethod
    def setMetadataTitle(self, value):
        pass

    @abstractmethod
    def setMetadataArtist(self, value):
        pass

    @abstractmethod
    def setMetadataAlbum(self, value):
        pass

    @abstractmethod
    def setMetadataDate(self, value):
        pass

    @abstractmethod
    def setMetadataDescription(self, value):
        pass

    @abstractmethod
    def setMetadataComment(self, value):
        pass

    def getMetadataField(self, field):
        try:
            return self.file[field][0]
        except:
            return ""

    def getAllFileMetadata(self):
        return self.file.pprint()

    def saveFileMetadata(self):
        self.file.save()
    
    def serializeToDictionary(self):
        updatedValues = {
            "title": self.getSongTitle(),
            "artist": self.getSongArtist(),
            "album": self.getSongAlbum(),
            "date": self.getSongDate()
        }
        successStatus = {"summary": ""}
        for key, value in updatedValues.items():
            if value == "":
                successStatus[key] = "Not Found"
            else:
                successStatus[key] = "Found"
        
        foundFlag = False
        notFoundFlag = False
        for key, value in successStatus.items():
            if value == "Found":
                foundFlag = True
            elif value == "Not Found":
                notFoundFlag = False
        if foundFlag and notFoundFlag:
            successStatus["summary"] = "partial"
        elif foundFlag and not notFoundFlag:
            successStatus["summary"] = "complete"
        else:
            successStatus["summary"] = "incomplete"

        return {
            "originalFilename": self.getFileLocation(),
            "originalValues": {
                "title": self.getOriginalTitle(),
                "uploader": self.getOriginalUploader(),
                "album": self.getOriginalAlbum(),
                "uploadDate": self.getOriginalUploadDate(),
                "URL": self.getOriginalURL()
            },
            "updatedValues": updatedValues,
            "successStatus": successStatus,
            "comment": "Some comment"
        }

    def getFileLocation(self):
        try:
            return self.fileLocation
        except:
            return ""

    def getOriginalTitle(self):
        try:
            return self.originalTitle
        except:
            return ""
    def getOriginalUploader(self):
        try:
            return self.originalUploader
        except:
            return ""
    def getOriginalAlbum(self):
        try:
            return self.originalAlbum
        except:
            return ""
    def getOriginalUploadDate(self):
        try:
            return self.originalUploadDate
        except:
            return ""
    def getOriginalURL(self):
        try:
            return self.originalURL
        except:
            return ""

    def getSongTitle(self):
        try:
            return self.SongTitle
        except:
            return ""
    def getSongArtist(self):
        try:
            return self.SongArtist
        except:
            return ""
    def getSongAlbum(self):
        try:
            return self.SongAlbum
        except:
            return ""
    def getSongDate(self):
        try:
            return self.SongDate
        except:
            return ""



class OGGFile(SongFile):
    def __init__(self, fileLocation, JSONDictionary):
        self.file = OggOpus(fileLocation)
        super().__init__(fileLocation, JSONDictionary)

    def initializeFileFields(self):
        self.originalTitle = self.getMetadataField("title")
        self.originalUploader = self.getMetadataField("artist")
        self.originalUploadDate = self.getMetadataField("date")
        self.originalComment = self.getMetadataField("comment")
        self.originalDescription = self.getMetadataField("description")
        self.originalURL = self.getMetadataField("purl")


    def setMetadataField(self, field, value):
        self.file[field] = value

    def setMetadataTitle(self, value):
        self.file["title"] = value

    def setMetadataArtist(self, value):
        self.file["artist"] = value

    def setMetadataAlbum(self, value):
        self.file["album"] = value

    def setMetadataDate(self, value):
        self.file["date"] = value

    def setMetadataDescription(self, value):
        self.file["description"] = value

    def setMetadataComment(self, value):
        self.file["comment"] = value


class MP4File(SongFile):
    def __init__(self, fileLocation, JSONDictionary):
        self.file = MP4(fileLocation)
        super().__init__(fileLocation, JSONDictionary)

    def initializeFileFields(self):
        self.originalTitle = self.getMetadataField("\xa9nam")
        self.originalUploader = self.getMetadataField("\xa9ART")
        self.originalUploadDate = self.getMetadataField("\xa9day")
        self.originalComment = self.getMetadataField("\xa9cmt")
        self.originalDescription = self.getMetadataField("desc")
        self.originalURL = self.getMetadataField("purl")

    def setMetadataField(self, field, value):
        self.file[field] = value

    def setMetadataTitle(self, value):
        self.file["\xa9nam"] = value

    def setMetadataArtist(self, value):
        self.file["\xa9ART"] = value

    def setMetadataAlbum(self, value):
        self.file["\xa9alb"] = value

    def setMetadataDate(self, value):
        self.file["\xa9day"] = value

    def setMetadataDescription(self, value):
        self.file["desc"] = value

    def setMetadataComment(self, value):
        self.file["\xa9cmt"] = value
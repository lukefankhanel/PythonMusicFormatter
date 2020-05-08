from mutagen.oggopus import OggOpus
      

def main():
    # audio = FLAC("example.flac")
    # audio["title"] = "An example"
    # audio.pprint()
    # audio.save()
    print("\nStarting Output\n")
    testfile = OggOpus("testfiles/musicfile.opus")
    testfile["DATE"] = "2018"
    #testfile.save()
    tagslist = testfile.tags
    for x in tagslist:
        print("\n" + x + "\n")

    print(testfile.pprint())



if __name__ == "__main__":
    main()
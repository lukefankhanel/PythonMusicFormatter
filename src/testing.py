from mutagen.oggopus import OggOpus
import tkinter

def main():
    # audio = FLAC("example.flac")
    # audio["title"] = "An example"
    # audio.pprint()
    # audio.save()

    # print("\nStarting Output\n")
    # testfile = OggOpus("testfiles/musicfile.opus")
    # testfile["DATE"] = "2018"
    # #testfile.save()
    # tagslist = testfile.tags
    # for x in tagslist:
    #     print("\n" + x + "\n")

    # print(testfile.pprint())
    window = tkinter.Tk()
    window.geometry("650x450+550+300")

    

    main = tkinter.Frame(master=window, relief=tkinter.RIDGE, borderwidth=10)
    two = tkinter.Frame(master=main, relief= tkinter.SUNKEN, borderwidth=5)
    three = tkinter.Frame(master=main, relief= tkinter.RAISED, borderwidth=5)

    hello = tkinter.Label(text="Hello World", master=two)
    label2 = tkinter.Label(text="Hello Opus", master=two)
    label3 = tkinter.Label(text="Hello Iao", master=two)
    label4 = tkinter.Label(text="Hello Lss", master=three)
    label5 = tkinter.Label(text="Hello Gsl", master=three)

    label5.pack()
    label4.pack()
    label3.pack()
    label2.pack()
    hello.pack()
    three.pack(side=tkinter.RIGHT)
    two.pack(side=tkinter.LEFT)
    main.pack(side=tkinter.BOTTOM)
    window.mainloop()



if __name__ == "__main__":
    main()
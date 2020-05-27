from mutagen.oggopus import OggOpus
import tkinter as tk

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
    # window = tkinter.Tk()
    # window.geometry("650x450+550+300")

    

    # main = tkinter.Frame(master=window, relief=tkinter.RIDGE, borderwidth=10)
    # two = tkinter.Frame(master=main, borderwidth=5)
    # two["bg"] = "Red"
    # two["relief"] = tkinter.RIDGE
    # two["pady"] = 100
    # two["padx"] = 100
    # #three = tkinter.Frame(master=main, relief= tkinter.RAISED, borderwidth=5)
    # three = create_frame_1()
    # three["master"] = main

    # hello = tkinter.Label(text="Hello World", master=two)
    # label2 = tkinter.Label(text="Hello Opus", master=two)
    # label3 = tkinter.Label(text="Hello Iao", master=two)
    # label4 = tkinter.Label(text="Hello Lss", master=three)
    # label5 = tkinter.Label(text="Hello Gsl", master=three)

    # label5.pack()
    # label4.pack()
    # label3.pack()
    # label2.pack()
    # hello.pack()
    # three.pack(side=tkinter.RIGHT)
    # two.pack(side=tkinter.LEFT)
    # main.pack(side=tkinter.BOTTOM)
    # window.mainloop()
    # main = MainWindow()
    # #main.mainloop()
    # dog = Dog("Doggo", 12)
    # dog.to_string()
    # dog.run()

    # ani = Animal("T", 3)
    # ani.run()

    window = MainWindow()
    window.mainloop()

    # d = Dog(age = 3, name = "Heee")
    # print(d.to_string())

class MainWindow(tk.Tk):

    def __init__(self):
        super().__init__()
        self.geometry("650x450+550+300")

        contain = tk.Frame(self)
        
        frame1 = MyFrame(contain, "Yellow") #self.create_frame_1()
        frame2 = MyFrame(None, "Blue")

        frame2.pack()
        contain.pack()
        frame1.pack()

    def create_frame_1(self):
        blue = MyFrame(self, "Blue")
        blue.master = self
        return blue

class MyFrame(tk.Frame):
    def __init__(self, parent, color):
        #TODO Does passing in just one argument implicitly assign it? eg. Dog(12)
        super().__init__(master = parent)
        self["bg"] = color
        self["padx"] = 100
        self["pady"] = 100
        self["relief"] = tk.GROOVE
        self["borderwidth"] = 5
        lab = tk.Label(text="Hello", master=self)
        lab.pack()
        #self.background = color



# class Animal():
#     name =""
#     age = 0

#     def __init__(self, name, age):
#         self.name = name
#         self.age = age

#     def run(self):
#         print("Animal is running")

#     def to_string(self):
#         print(self.name + " " + str(self.age))

# class Dog(Animal):
#     def __init__(self, name, age):
#         super().__init__(name, age)

#     def run(self):
#         print("Dog is running")



# def create_frame_1():
#     frame = tkinter.Frame()

#     frame["bg"] = "Yellow"
#     frame["relief"] = tkinter.GROOVE
#     frame["bd"] = 5
#     frame["padx"] = 50
#     return frame



if __name__ == "__main__":
    main()
import tkinter


def initialize_gui():
    global window, main_frame

    window = tkinter.Tk()
    window.geometry("650x450+550+300")

    main_frame = tkinter.Frame()
    main_frame.pack()

def main():
    
    initialize_gui()

    window.mainloop()

if __name__ == "__main__":
    main()
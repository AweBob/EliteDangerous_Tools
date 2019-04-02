import tkinter
from tkinter import *
print('Library import sucessful!')

#This is a server side acessory for processing data
#Features: merges temp file/files and final file, displays data in temp file, displays final data
#Run this in the same directory you ran the server in, this ensures it finds the proper files

def mainCode () :
    print('d = display final' + '\n' + 'm = merge' + '\n' + 't = display temp' + '\n')
    whatYouWannaDo = input('What do you want to do - ')
    if whatYouWannaDo == 'd' :
        displayFinal()
    elif whatYouWannaDo == 'm' :
        mergeFiles()
    elif whatYouWannaDo == 't' :
        displayTemp()
    else :
        print('Really? Try again :p' + '\n')
        mainCode()

def displayFinal () :
    root = Tk()
    ui = displayFinalInterface( root )
    root.mainloop()

def mergeFiles () :
    foo = 'bar'

def displayTemp () :
    try :
        textFile = open('ServerOutput.txt','r')
    except :
        print('Output file isnt in this directory, try again!' + '\n')
        mainCode()
    root = Tk()
    ui = displayTempInterface( root )
    root.mainloop()



class displayFinalInterface :
    def __init__(self, master):
        self.master = master
        master.title("Event data")

        self.label = Label(master, text="foobar")
        self.label.pack()

class displayTempInterface :
    def __init__(self, master):
        self.master = master
        master.title("Stuff")

        self.label = Label(master, text="foobar")
        self.label.pack()



mainCode()
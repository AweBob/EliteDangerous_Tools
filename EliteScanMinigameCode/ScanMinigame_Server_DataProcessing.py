


#THIS ISN'T DONE
#THIS IS USELESS, MERELY AN IDEA
#EASILY DONE BY A HUMAN, i'LL JUST DO IT MYSELF, THE FORMAT OF THE OUTPUT FILE IS SO EASY TO READ
#NO NEED FOR THIS, AND JUST ANOTHER THING TO TEST


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
    try :
        textFile = open('ServerOutput.txt','r') #noit correct
    except :
        print('Output file isnt in this directory, try again!' + '\n')
        mainCode()
    with textFile as tf :
        contentList = []
        for line in tf :
            contentList.append( line )
    

    root = Tk()
    ui = displayFinalInterface( root )
    root.mainloop()

def mergeFiles () :
    foo = 'bar'

def displayTemp () :
    try :
        textFile = open('ServerOutput.txt','r') #not correct
    except :
        print('Output file isnt in this directory, try again!' + '\n')
        mainCode()
    with textFile as tf :
        contentList = tf.read().splitlines()
    for item in contentList :
        foo = 'bar' #placeholde

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
import tkinter

def ende():
    main.destroy()

def anzeigen():
    lb["text"] = "Auswahl: " + farbe.get()

main = tkinter.Tk()

farbe = tkinter.StringVar()
farbe.set("rot")

rb1 = tkinter.Radiobutton(main,text="rot",value="rot",variable=farbe,command=anzeigen)
rb2 = tkinter.Radiobutton(main,text="gruen",value="gruen",variable=farbe,command=anzeigen)
rb3 = tkinter.Radiobutton(main,text="gelb",value="gelb",variable=farbe,command=anzeigen)

rb1.pack()
rb2.pack()
rb3.pack()

lb = tkinter.Label(main, text ="Auswahl: ")
lb.pack()

bende = tkinter.Button(main,text="Ende",command=ende)
bende.pack()

main.mainloop()
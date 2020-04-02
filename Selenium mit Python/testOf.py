import tkinter

def ende():
    main.destroy()

main = tkinter.Tk()

b = tkinter.Button(main, text = "Ende", command = ende)
b.pack()

main.mainloop()

print("Testausgabe fuer PyCharm und Git")

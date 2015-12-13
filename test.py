from tkinter import *
root = Tk()
 
afficheur = Label(root, text="Cliquer pour tester", bg="white")
afficheur.pack(side=TOP, expand=TRUE)
 
Button(root, text="Test 1", relief="flat", command=lambda: afficheur.config(text="Test1")).pack(side=LEFT)
 
Button(root, text="Test 2", relief="flat", borderwidth=0, command=lambda: afficheur.config(text="Test2")).pack(side=LEFT)
 
Button(root, text="Test 3", relief="flat", borderwidth=0, highlightthickness=0, command=lambda: afficheur.config(text="Test3")).pack(side=LEFT)
 
lab=Label(root, text="Test 4")
lab.pack(side=LEFT)
lab.bind("<ButtonPress-1>", lambda event: afficheur.config(text="Test4"))
 
root.mainloop()

import tkinter as tk

master = tk.Tk()
master.minsize(300,100)
master.geometry("320x100")

def callback():
	print("click!")

frame = tk.Frame(master)

photo=tk.PhotoImage(file="C:\\Projetos\\UpdEnv\\imagens\\find.gif")
b = tk.Button(frame,image=photo, height=50, width=150, compound=tk.LEFT)
frame.pack()

tk.mainloop()
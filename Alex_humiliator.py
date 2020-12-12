import tkinter as tk

auto_counter = 5
def Alex():
    i = tk.Tk()
    tk.Message(i, text = "Alex is humiliated",width = 200).grid()
    i.mainloop()

def auto():
    global auto_counter
    if auto_counter >= 1:
        auto_counter -= 1
        i = tk.Tk()
        tk.Message(i, text = "But Alex is too lazy to autonomously humiliate himself...",bd = 10).pack()
        i.mainloop()
    else:
        count = int(ent.get())
        for i in range(count):
            Alex()

root = tk.Tk()
frame = tk.Frame(root)
frame.grid(row = 1,column=0)
tk.Button(frame,text="Humiliate",fg = "red",command = Alex).grid(row = 1,column=0)
tk.Button(frame,text="Auto", fg = "blue",command = auto).grid(row = 1,column=1)
tk.Button(frame,text="Quit",command = quit).grid(row = 1,column=2)
ent = tk.Entry(root)
ent.grid(row=0,column=0)

root.mainloop()


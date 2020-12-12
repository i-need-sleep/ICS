from tkinter import *
import chat_cmdl_client as cmdl
from tkinter.messagebox import *
from tkinter.colorchooser import askcolor
from tkinter.filedialog import askopenfilename 
from tkinter.filedialog import askdirectory
from tkinter import simpledialog    
import client_state_machine as csm  
import json
from chat_utils import *
import time
import bullet_hell
import bullet_hell_autoplay
LaunchState = False
DarkMode = False
PastaMode = False
AutoScroll = True
username = 'username'

#Basic functions
def update_username(name):
    global username
    T2.delete(1.0,END)
    username = name
    T2.insert(END,name+":\n")
    
def display(who,input_text):
    T.config(state=NORMAL)
    T.insert(END,"\n["+ who + "]:" + input_text)
    root.update_idletasks()
    T.config(state=DISABLED)
    if AutoScroll == True:
        T.see(END)
    
#handles message entry
def enter(event):
    input_text = T2.get(2.0,END)[:-1]
    display(username," "+input_text)
    cmdl.client.GUI_input = input_text
    T2.delete(2.0,END)
    
def button_enter():
    input_text = T2.get(2.0,END)[:-1]
    display(username," "+input_text)
    cmdl.client.GUI_input = input_text
    T2.delete(2.0,END)
    if cmdl.client.sm.state != S_OFFLINE:
        T2.insert(END,"\n")
    
def launch(event):
    global LaunchState
    if LaunchState == False:
        T.config(state=NORMAL)
        T.insert(END,"Launching...")
        T.config(state=DISABLED)
        print("launching main module")
        LaunchState = True
        cmdl.main()
    
#creates the chat window, T=textdisplay T2=entry
root = Tk()
root.title("La Pasta de Chatto")
S = Scrollbar(root)
T = Text(root, height=25, width=80)
S.grid(row=0,column=1,sticky="ns")
T.grid(row=0,column=0)
S.config(command=T.yview)
T.config(yscrollcommand=S.set)
T.config(state=DISABLED)
S2 = Scrollbar(root)
T2 = Text(root, height=15, width=80)
S2.grid(row=1,column=1,sticky="ns")
T2.grid(row=1,column=0)
S2.config(command=T.yview)
T2.config(yscrollcommand=S.set)
T2.bind('<Return>', enter)
T.bind('<Enter>', launch)
T2.bind('<Enter>', launch)
T2.insert(END,"username:\n")
T.see(END)

send_button = Button(root, text="Send", width = 20, command=button_enter)
send_button.grid(row=2,column=0)

#Menu Functions
def Quit():
    if askyesno('Quitting', 'Really quit?'):
        if cmdl.client.sm.state == csm.S_OFFLINE:
            root.destroy()
        else:
            cmdl.client.GUI_input = 990
def Color_T():
    result = askcolor(color="#6A9662",title = "Colour Chooser") 
    T.config(bg=result[-1])
    global DarkMode
    DarkMode = False
    global PastaMode
    PastaMode = False
    
def Color_T2():
    result = askcolor(color="#6A9662",title = "Colour Chooser") 
    T2.config(bg=result[-1])
    global DarkMode
    DarkMode = False
    global PastaMode
    PastaMode = False
    
def Color_t():
    result = askcolor(color="#6A9662",title = "Colour Chooser") 
    T.config(fg=result[-1])
    global DarkMode
    DarkMode = False
    global PastaMode
    PastaMode = False
    
def Color_t2():
    result = askcolor(color="#6A9662",title = "Colour Chooser") 
    T2.config(fg=result[-1])
    global DarkMode
    DarkMode = False
    global PastaMode
    PastaMode = False
    
def Dark():
    global DarkMode
    global PastaMode
    PastaMode = False
    if DarkMode == False:
        DarkMode = True
        T.config(bg="black",fg="white")
        T2.config(bg="black",fg="white")
    elif DarkMode == True:
        DarkMode = False
        T.config(bg="white",fg="black")
        T2.config(bg="white",fg="black")
    
def Pasta():
    global DarkMode
    global PastaMode
    DarkMode = False
    if PastaMode == False:
        PastaMode = True
        T.config(bg="red",fg="yellow")
        T2.config(bg="yellow",fg="red")
        send_button.config(bg="red",fg="yellow")
    elif PastaMode == True:
        PastaMode = False
        T.config(bg="white",fg="black")
        T2.config(bg="white",fg="black")
        send_button.config(bg="white",fg="black")

def Time():
    cmdl.client.GUI_input = 1

def Who():
    cmdl.client.GUI_input = 2

def QuitChat():
    if cmdl.client.sm.state == csm.S_CHATTING:
        cmdl.client.GUI_input = 999
    else:
        display("system","but you are not in a chat now...")
    
def Poem():
    cmdl.client.sm.poem_num = simpledialog.askinteger("Poem", "Enter poem number (1~154)",
                                 parent=root,
                                 minvalue=1, maxvalue=154)
    cmdl.client.GUI_input = 3

def Connect_ini():
    cmdl.client.GUI_input = 4

class call:
    def __init__(self,name,connect_selector):
        self.name = name
        self.connect_selector = connect_selector
        Button(connect_selector, text = name,command = self.connect).pack()
    def connect(self):
        cmdl.client.GUI_input ="c " + self.name
        self.connect_selector.destroy()

def Connect_menu(In):
    connect_selector = Tk()
    connect_selector.title("Connect")
    UserList = str(In.split("\n")[1])[1:-1].split(",")
    c = 0
    c2 = 0
    for i in UserList:
        User = i.split(":")[0].lstrip(" ")[1:-1]
        if c2 == 0 and User != username:
            Label(connect_selector,text = "Select a user:").pack()
            c2 += 1
        if User != username:
            c += 1
            call(User,connect_selector)
    if c == 0:
        Label(connect_selector,text = "No other user found!").pack()
        
def Search():
    cmdl.client.sm.search = simpledialog.askstring("Search", "Enter keyword(s)",
                                 parent=root)
    cmdl.client.GUI_input = 5
    
def Preference():
    global ResizeX
    global ResizeTY 
    global ResizeT2Y
    global pref_menu
    pref_menu = Tk()
    pref_menu.title("Preference")
    
    #AutoScroll
    CheckAutoScroll = Checkbutton(pref_menu, text="Auto Scroll",command = SwitchAutoScroll)
    CheckAutoScroll.grid(row=0,column=0,columnspan=2)
    if AutoScroll == True:
        CheckAutoScroll.select()
    
    #WindowResize
    ResizeXM = Label(pref_menu,text="Resize X:")
    ResizeXM.grid(row=1,column=0)
    ResizeX = Text(pref_menu,height=1,width=5)
    ResizeX.grid(row=1,column=1)
    ResizeTYM = Label(pref_menu,text="Resize Y (Display):")
    ResizeTYM.grid(row=2,column=0)
    ResizeTY = Text(pref_menu,height=1,width=5)
    ResizeTY.grid(row=2,column=1)
    ResizeT2YM = Label(pref_menu,text="Resize Y (Entry):")
    ResizeT2YM.grid(row=3,column=0)
    ResizeT2Y = Text(pref_menu,height=1,width=5)
    ResizeT2Y.grid(row=3,column=1)
    ResizeB = Button(pref_menu,text="Apply Resize",command=Resize)
    ResizeB.grid(row=4,column=0,columnspan=2)
    
    #Update default folder for file trasfer
    Label(pref_menu,text="File transfer folder: ").grid(row=5,column=0)
    Button(pref_menu,text="Select",command=update_trans_dir).grid(row=5,column=1)

def SwitchAutoScroll():
    global AutoScroll
    AutoScroll = not AutoScroll
    
def Resize():
    X = ResizeX.get(0.0,END)
    YT = ResizeTY.get(0.0,END)
    YT2 = ResizeT2Y.get(0.0,END)
    c = 0
    try:
        T.config(width=X)
        T2.config(width=X)
    except:
        c += 1
    try:
        T.config(height = YT)
    except:
        c += 1
    try:
        T2.config(height = YT2)
    except:
        c += 1
    if c == 3:
        display("resize","no valid input!")
            
def SendFile():
    try:
        cmdl.client.sm.file_dir = askopenfilename()
    except:
        pass
    cmdl.client.GUI_input = 6
    
def update_trans_dir():
    global pref_menu
    cmdl.client.sm.file_receive = askdirectory()
    pref_menu.destroy()
    
def About():
    display("system","""About:
            La Pasta de Chatto\n
                           ^(Yes, we know that's not a real word)\n
            Copyright lolol\n
            Created (? or modified or upgraded or watever) by Will and Ryan\n
            Title credit to: La Pasta and Ryan's pasta-like code\n
            oh and also...\n
            ...RYAN MUST DIE\n
            that's all. thank you...\n
            """)
#Game functions:  
def game_start():
    bullet_hell.start()


def leaderboard_submit():
    if cmdl.client.sm.state == csm.S_OFFLINE:
        display("system","Please log in first...")
    else:
        if askyesno('Submit high score', 'Your highscore is: '+str(cmdl.client.sm.high_score)+"\nSubmit?"):
            cmdl.client.GUI_input = 7
        #In the case the leaderboard window is open
        #Destroy the window, and open a new one
        try:
            ldb_tab.destroy()
            leaderboard_update()
        except:
            pass
            
def leaderboard_view():
    cmdl.client.GUI_input = 8

def leaderboard_update():
    cmdl.client.GUI_input = 9
    
def display_leaderboard(ldb):
    global ldb_tab
    if len(ldb) == 0:
        leader_text = "No submitted socres...\nWhy don't YOU be the first one on the board?"
    else:
        leader_text = ""
        leaders = sorted(ldb,key = ldb.get)
        leaders.reverse()
        c = 0
        for i in leaders:
            if c == 0:
                first_text = i + ": " + str(ldb[i])
                c += 1
            else:
                leader_text += i + ": " + str(ldb[i]) + "\n"
    ldb_tab = Tk()
    ldb_tab.title("Leaderboard")
    Label(ldb_tab,text="LEADERBOARD",font="Helvetica 16 bold italic",fg="blue").pack()
    if len(ldb) != 0:
        Label(ldb_tab,text=first_text,font="Helvetica 12 bold",fg="red").pack()
    if len(ldb) != 1:
        Label(ldb_tab,text=leader_text.rstrip("\n"),font="Calibri 11").pack()
    Button(ldb_tab,text="Submit my high score",command = leaderboard_submit).pack()

def game_autoplay():
    bullet_hell_autoplay.start()

def game_about():
    game_about_msg = """ Bullet Hell
         About this game
         This game is the second choice I made 
         after I failed to make a bullet shooting game like touhou project.
         I have put many memes in this game(要 素 过 多）for you to find out, 
         hope you enjoy the game! BTW the extreme mode is not for human,
         and WILL MUST DIE                                          --Ryan

         Base game implementation by Ryan
         Leaderboard implementation, game integration into the chat system
         and enduring Ryan in general... by Will
         
         ...and the joke's on you, Ryan. 
         This is MY about message..."""
    display("system",game_about_msg)
        
menu = Menu(root)
root.config(menu=menu)
filemenu = Menu(menu)
gamemenu = Menu(menu)
helpmenu = Menu(menu)

#File menu (Function menu)
menu.add_cascade(label="Functions",menu=filemenu)
menu.add_cascade(label="Game",menu=gamemenu)
menu.add_cascade(label="Options",menu=helpmenu)
filemenu.add_command(label="Time",command=Time)
filemenu.add_command(label="Show active users",command=Who)
filemenu.add_command(label="Poem",command=Poem)
filemenu.add_command(label="Search",command=Search)
filemenu.add_separator()
filemenu.add_command(label="File transfer",command=SendFile)
filemenu.add_separator()
filemenu.add_command(label="Connect",command=Connect_ini)
filemenu.add_command(label="Quit chat",command=QuitChat)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=Quit)

#Game menu
gamemenu.add_command(label="Play",command=game_start)
leaderboard_menu = Menu(menu)
gamemenu.add_command(label="Auto play",command=game_autoplay)
gamemenu.add_cascade(label="Leaderboard",menu=leaderboard_menu)
leaderboard_menu.add_command(label="View",command=leaderboard_view)
leaderboard_menu.add_command(label="Submit",command=leaderboard_submit)
gamemenu.add_separator()
gamemenu.add_command(label="About...",command=game_about)

#Help menu (Options menu)
bkg=Menu(menu)
helpmenu.add_cascade(label="Change background color",menu=bkg)
bkg.add_command(label="Display",command=Color_T)
bkg.add_command(label="Input",command=Color_T2)
Tex=Menu(menu)
helpmenu.add_cascade(label="Change text color",menu=Tex)
Tex.add_command(label="Display",command=Color_t)
Tex.add_command(label="Input",command=Color_t2)
helpmenu.add_command(label="Dark mode",command=Dark)
helpmenu.add_command(label="Pasta Mode",command=Pasta)
helpmenu.add_command(label="Preference",command=Preference)
helpmenu.add_separator()
helpmenu.add_command(label="About...", command=About)


#for debugging purposes
if __name__ == "__main__":
    mainloop(  )
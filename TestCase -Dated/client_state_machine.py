"""
Created on Sun Apr  5 00:00:32 2015

@author: zhengzhang
"""
from chat_utils import *
import json
import chatGUI as GUI
import base64
codec = "utf-8"

class ClientSM:
    def __init__(self, s):
        self.state = S_OFFLINE
        self.peer = ''
        self.me = ''
        self.out_msg = ''
        self.s = s
        self.poem_num = 1
        self.search = ''
        self.file_dir = ''
        self.file_receive = "D:/"
        self.high_score = 0

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state

    def set_myname(self, name):
        self.me = name

    def get_myname(self):
        return self.me

    def connect_to(self, peer):
        msg = json.dumps({"action":"connect", "target":peer})
        mysend(self.s, msg)
        response = json.loads(myrecv(self.s))
        if response["status"] == "success":
            self.peer = peer
            self.out_msg += 'You are connected with '+ self.peer + '\n'
            return (True)
        elif response["status"] == "busy":
            self.out_msg += 'User is busy. Please try again later\n'
        elif response["status"] == "self":
            self.out_msg += 'Cannot talk to yourself (sick)\n'
        else:
            self.out_msg += 'User is not online, try again later\n'
        return(False)

    def disconnect(self):
        msg = json.dumps({"action":"disconnect"})
        mysend(self.s, msg)
        self.out_msg += 'You are disconnected from ' + self.peer + '\n'
        self.peer = ''
    
    def poem(self):
        poem_idx = self.poem_num
        mysend(self.s, json.dumps({"action":"poem", "target":poem_idx}))
        poem = json.loads(myrecv(self.s))["results"]
        if (len(poem) > 0):
            self.out_msg += poem + '\n\n'
        else:
            self.out_msg += 'Sonnet ' + poem_idx + ' not found\n\n'
    
    def SendFile(self):
        FO = open(self.file_dir,"rb")
        FileMsg = base64.b64encode(FO.read())
        FileMsg = FileMsg.decode(codec)
        FO.close()
        file_name = self.file_dir.split("/")[-1]
        msg = "Sent file: " + file_name
        Out = {"action":"file", "from":"[" + self.me + "]", "message":msg,"file":FileMsg,"file_name":file_name}
        mysend(self.s, json.dumps(Out))
        self.out_msg += "[" + self.me + "]" + ": Sending File: " + self.file_dir
        self.out_msg += json.loads(myrecv(self.s))["results"]
        
    def submit_highscore(self):
        mysend(self.s, json.dumps({"action":"submit_highscore", "score":self.high_score,"player":self.me}))
        self.out_msg += json.loads(myrecv(self.s))["results"]
        
    def view_leaderboard(self):
        mysend(self.s, json.dumps({"action":"view_leaderboard"}))
        GUI.display_leaderboard(json.loads(myrecv(self.s))["results"])
        
    def update_leaderboard(self):
        self.submit_highscore()
        self.view_leaderboard()
                
    def proc(self, my_msg, peer_msg):
        self.out_msg = ''
#==============================================================================
# Once logged in, do a few things: get peer listing, connect, search
# And, of course, if you are so bored, just go
# This is event handling instate "S_LOGGEDIN"
#==============================================================================
        if self.state == S_LOGGEDIN:
            # todo: can't deal with multiple lines yet
            if type(my_msg) == str:
                if len(my_msg) > 0:
    
                    if my_msg == 'q':
                        self.out_msg += 'See you next time!\n'
                        self.state = S_OFFLINE
                        GUI.root.destroy()
    
                    elif my_msg == 'time':
                        mysend(self.s, json.dumps({"action":"time"}))
                        time_in = json.loads(myrecv(self.s))["results"]
                        self.out_msg += "Time is: " + time_in
    
                    elif my_msg == 'who':
                        mysend(self.s, json.dumps({"action":"list"}))
                        logged_in = json.loads(myrecv(self.s))["results"]
                        self.out_msg += 'Here are all the users in the system:\n'
                        self.out_msg += logged_in
    
                    elif my_msg[0] == 'c':
                        peer = my_msg[1:]
                        peer = peer.strip()
                        if self.connect_to(peer) == True:
                            self.state = S_CHATTING
                            self.out_msg += 'Connect to ' + peer + '. Chat away!\n\n'
                            self.out_msg += '-----------------------------------\n'
                        else:
                            self.out_msg += 'Connection unsuccessful\n'
    
                    elif my_msg[0] == '?':
                        term = my_msg[1:].strip()
                        mysend(self.s, json.dumps({"action":"search", "target":term}))
                        search_rslt = json.loads(myrecv(self.s))["results"].strip()
                        if (len(search_rslt)) > 2:
                            self.out_msg += search_rslt + '\n\n'
                        else:
                            self.out_msg += '\'' + term + '\'' + ' not found\n\n'
    
                    elif my_msg[0] == 'p' and my_msg[1:].isdigit():
                        poem_idx = my_msg[1:].strip()
                        mysend(self.s, json.dumps({"action":"poem", "target":poem_idx}))
                        poem = json.loads(myrecv(self.s))["results"]
                        if (len(poem) > 0):
                            self.out_msg += poem + '\n\n'
                        else:
                            self.out_msg += 'Sonnet ' + poem_idx + ' not found\n\n'
    
                    else:
                        self.out_msg += menu
            elif type(my_msg) == int:
                if my_msg == 1:
                    mysend(self.s, json.dumps({"action":"time"}))
                    time_in = json.loads(myrecv(self.s))["results"]
                    self.out_msg += "Time is: " + time_in
                elif my_msg == 2:
                    mysend(self.s, json.dumps({"action":"list"}))
                    logged_in = json.loads(myrecv(self.s))["results"]
                    self.out_msg += 'Here are all the users in the system:\n'
                    self.out_msg += logged_in
                elif my_msg == 3:
                    self.poem()
                elif my_msg == 4:
                    mysend(self.s, json.dumps({"action":"list"}))
                    logged_in = json.loads(myrecv(self.s))["results"]
                    GUI.Connect_menu(logged_in)
                elif my_msg == 5:
                    term = self.search
                    mysend(self.s, json.dumps({"action":"search", "target":term}))
                    search_rslt = json.loads(myrecv(self.s))["results"].strip()
                    if (len(search_rslt)) > 2:
                        self.out_msg += search_rslt + '\n\n'
                    else:
                        self.out_msg += '\'' + term + '\'' + ' not found\n\n'
                elif my_msg == 6:
                    self.out_msg += "Join a chat first!"
                elif my_msg == 7:
                    self.submit_highscore()
                elif my_msg == 8:
                    self.view_leaderboard()
                elif my_msg == 9:
                    self.update_leaderboard()
                elif my_msg == 990:
                    self.out_msg += 'See you next time!\n'
                    self.state = S_OFFLINE
                    GUI.root.destroy()

            if len(peer_msg) > 0:
                try:
                    peer_msg = json.loads(peer_msg)
                except Exception as err :
                    self.out_msg += " json.loads failed " + str(err)
                    return self.out_msg
            
                if peer_msg["action"] == "connect":

                    # ----------your code here------#
                    from_name = peer_msg["from"]
                    self.state = S_CHATTING
                    self.out_msg += "connected to " + str(from_name) + "\n-----------------------------------\n"
                    # ----------end of your code----#
                    
#==============================================================================
# Start chatting, 'bye' for quit
# This is event handling instate "S_CHATTING"
#==============================================================================
        elif self.state == S_CHATTING:
            if type(my_msg) == str:
                if len(my_msg) > 0:     # my stuff going out
                    mysend(self.s, json.dumps({"action":"exchange", "from":"[" + self.me + "]", "message":my_msg}))
                    #bye is disabled, use quit chat function in the functions menu instead
                        
                    
            elif my_msg == 1:
                mysend(self.s, json.dumps({"action":"time"}))
                time_in = json.loads(myrecv(self.s))["results"]
                self.out_msg += "Time is: " + time_in
            elif my_msg == 2:
                mysend(self.s, json.dumps({"action":"list"}))
                logged_in = json.loads(myrecv(self.s))["results"]
                self.out_msg += 'Here are all the users in the system:\n'
                self.out_msg += logged_in
            elif my_msg == 3:
                self.poem()
            elif my_msg == 4:
                self.out_msg += 'Quit chat first!'
            elif my_msg == 5:
                term = self.search
                mysend(self.s, json.dumps({"action":"search", "target":term}))
                search_rslt = json.loads(myrecv(self.s))["results"].strip()
                if (len(search_rslt)) > 2:
                    self.out_msg += search_rslt + '\n\n'
                else:
                    self.out_msg += '\'' + term + '\'' + ' not found\n\n'
            elif my_msg == 6:
                self.SendFile()
            elif my_msg == 7:
                self.submit_highscore()
            elif my_msg == 8:
                self.view_leaderboard()
            elif my_msg == 9:
                self.update_leaderboard()
            elif my_msg == 999:
                print("disconnecting")
                self.disconnect()
                self.state = S_LOGGEDIN
                self.peer = ''
            elif my_msg == 990:
                print("disconnecting")
                self.disconnect()
                self.state = S_LOGGEDIN
                self.peer = ''
                self.out_msg += 'See you next time!\n'
                self.state = S_OFFLINE
                GUI.root.destroy()
                    
            if len(peer_msg) > 0:    # peer's stuff, coming in
  

                # ----------your code here------#
                peer_msg = json.loads(peer_msg)
                if peer_msg["action"] == "exchange":
                    from_name = str(peer_msg["from"])
                    self.out_msg += from_name + ": " + peer_msg["message"]
                elif peer_msg["action"] == "connect":
                    from_name = peer_msg["from"]
                    self.out_msg += "connected to " + str(from_name) + "\n-----------------------------------\n"
                elif peer_msg["action"] == "disconnect":
                    self.out_msg += "disconnect from chat"
                    self.state = S_LOGGEDIN
                # ----------end of your code----#
                
                #Receving file!!
                elif peer_msg["action"] == "file":
                    from_name = str(peer_msg["from"])
                    self.out_msg += from_name + ": " + peer_msg["message"] + "\n" + " " * (len(from_name) + 2) + "Saved at: " + self.file_receive
                    FO = open(self.file_receive+"/"+peer_msg["file_name"],"wb")
                    bin_data = bytes(peer_msg['file'],codec)
                    FO.write(base64.b64decode(bin_data))
                    FO.close()
                
            # Display the menu again
            if self.state == S_LOGGEDIN:
                self.out_msg += menu
#==============================================================================
# invalid state
#==============================================================================
        else:
            self.out_msg += 'How did you wind up here??\n'
            print_state(self.state)

        return self.out_msg

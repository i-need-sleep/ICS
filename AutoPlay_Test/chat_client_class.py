import time
import socket
import select
import sys
import json
from chat_utils import *
import client_state_machine as csm
import chatGUI as GUI

import threading

class Client:
    def __init__(self, args):
        self.peer = ''
        self.console_input = []
        self.state = S_OFFLINE
        self.system_msg = ''
        self.local_msg = ''
        self.peer_msg = ''
        self.args = args
        self.GUI_input = ''
        
    def quit(self):
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()

    def get_name(self):
        print("name: ",self.name)
        return self.name

    def init_chat(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM )
        svr = SERVER if self.args.d == None else (self.args.d, CHAT_PORT)
        self.socket.connect(svr)
        self.sm = csm.ClientSM(self.socket)
        reading_thread = threading.Thread(target=self.read_input)
        reading_thread.daemon = True
        reading_thread.start()

    def shutdown_chat(self):
        return

    def send(self, msg):
        mysend(self.socket, msg)

    def recv(self):
        return myrecv(self.socket)

    def get_msgs(self):
        read, write, error = select.select([self.socket], [], [], 0)
        my_msg = ''
        peer_msg = []
        #peer_code = M_UNDEF    for json data, peer_code is redundant
        try:
            GUI.root.update()
        except:
            pass
        if type(self.GUI_input) == str:
            if len(self.GUI_input) > 0:
                my_msg = self.GUI_input
                print(my_msg)
        elif type(self.GUI_input) == int:
            my_msg = self.GUI_input
            print(my_msg)
        if self.socket in read:
            peer_msg = self.recv()
        self.GUI_input = ''
        return my_msg, peer_msg

    def GUI_display(self,system_msg):
        GUI.T.config(state=GUI.NORMAL)
        GUI.T.insert(GUI.END,"\n" + system_msg)
        GUI.LastMsg = system_msg
        GUI.T.config(state=GUI.DISABLED)
        if GUI.AutoScroll == True:
            GUI.T.see(GUI.END)
        GUI.root.update()
        
    def output(self):
        try:
            if len(self.system_msg) > 0:
                print(self.system_msg)
                self.GUI_display(self.system_msg)
                self.system_msg = ''
        except:
            pass
            

    def login(self):
        my_msg, peer_msg = self.get_msgs()
        if type(my_msg) == str:
            if len(my_msg) > 0:
                self.name = my_msg
                GUI.update_username(self.name)
                msg = json.dumps({"action":"login", "name":self.name})
                self.send(msg)
                response = json.loads(self.recv())
                if response["status"] == 'ok':
                    self.state = S_LOGGEDIN
                    self.sm.set_state(S_LOGGEDIN)
                    self.sm.set_myname(self.name)
                    self.print_instructions()
                    return (True)
                elif response["status"] == 'duplicate':
                    self.system_msg += 'Duplicate username, try again'
                    return False
        elif type(my_msg) == int:
            self.GUI_display("Please log in first!")
            return(False)
        else:               # fix: dup is only one of the reasons
            return(False)


    def read_input(self):
        while True:
            text = sys.stdin.readline()[:-1]
            self.console_input.append(text) # no need for lock, append is thread safe

    def print_instructions(self):
        self.system_msg += menu

    def run_chat(self):
        self.init_chat()
        self.system_msg += 'Welcome to Pasta Chat\n'
        self.system_msg += 'Please enter your name: '
        self.output()
        while self.login() != True:
            self.output()
        self.system_msg += 'Welcome, ' + self.get_name() + '!'
        self.output()
        while self.sm.get_state() != S_OFFLINE:
            self.proc()
            self.output()
            time.sleep(CHAT_WAIT)
        self.quit()

#==============================================================================
# main processing loop
#==============================================================================
    def proc(self):
        my_msg, peer_msg = self.get_msgs()
        self.system_msg += self.sm.proc(my_msg, peer_msg)

from chatGUI import *
from chat_client_class import *

def main():
    print("launching")
    import argparse
    parser = argparse.ArgumentParser(description='chat client argument')
    parser.add_argument('-d', type=str, default=None, help='server IP addr')
    args = parser.parse_args()
    
    global client
    client = Client(args)
    client.run_chat()

if __name__ == "__main__":
    mainloop()
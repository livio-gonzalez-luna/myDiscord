from DbManager import *
from threading import *
import socket, pyaudio





class Server:
    def __init__(self):

        '''---------------SERVER GLOBALS---------------'''

        self.__IP = socket.gethostbyname(socket.gethostname())
        self.__PORT = 5050
        self.__HEADER = 64
        self.__FORMAT = "utf-8"
        self.__DISCONNECTION_SIGNAL = "DISCONNECT"

        self.__server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__server.bind((self.__IP, self.__PORT))

        self.__clients = []



        '''---------------DATABASE GLOBALS---------------'''

        #self.__users = CRUD(DB_CURSOR, "users")
        #self.__rooms = CRUD(DB_CURSOR, "rooms")

        #self.__usersColumns = self.__users.GetTableColumns()
        #self.__roomsColumns = self.__rooms.GetTableColumns()
    



    """Public methods"""


    def Run(self):
        self.__server.listen()
        print(f"Server listening on {self.__IP}")

        while True:
            clientSocket, clientIP = self.__server.accept()
            print(clientSocket, clientIP)

            thread = Thread(target=self.__ThreadedClient, args=(clientSocket, clientIP))
            thread.start()




    """Private methods"""


    def __ThreadedClient(self, socket:socket, ip):
        print(f"{ip} Connected")
        clientConnected = True

        while clientConnected:
            clientData = socket.recv(self.__HEADER).decode(self.__FORMAT)

            if clientData:
                clientData = int(clientData)
                data = socket.recv(clientData).decode(self.__FORMAT)

                if data == self.__DISCONNECTION_SIGNAL:
                    clientConnected = False

                print(f"[{ip}]: {data}")


        socket.close()



    def __RoomMessages(self):
        return None
    


    def __LoginCheck(self):
        return None








if __name__ == "__main__":
    server = Server()
    server.Run()
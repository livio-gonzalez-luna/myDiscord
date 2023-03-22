import socket, pyaudio, threading



class Client:
    def __init__(self):

        '''---------------CLIENT GLOBALS---------------'''

        self.__SERVER = "192.168.137.1"
        self.__PORT = 5050
        self.__HEADER = 64
        self.__FORMAT = "utf-8"

        self.__client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__client.connect((self.__SERVER, self.__PORT))




    """Public methods"""


    def ClientLogin(self, credentials:tuple):
        return None
    


    def Post(self, msg:str):
        post = msg.encode(self.__FORMAT)
        dataLength = len(post)

        postData = str(dataLength).encode(self.__FORMAT)
        postData += b' ' * (self.__HEADER - len(postData))

        self.__client.send(postData)
        self.__client.send(post)


    
    def NewUser(self):
        return None
import socket, pyaudio, json



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


    def ClientLogin(self, credentials:dict):
        userCredentials = self.__DataFormatting(credentials)
        print(userCredentials, type(userCredentials))
        
        self.__client.sendall(userCredentials)

        #self.__client.recv(1024)
    


    def MessagePost(self, msg:str):
        userMessage, messageData = self.__DataFormatting(msg)

        self.__client.send(messageData)
        self.__client.send(userMessage)

        #self.__client.recv(1024)


    
    def NewUser(self, newCredentials:dict):
        newUser = self.__DataFormatting(newCredentials)

        self.__client.send(newUser)
        
        #self.__client.recv(1024)
    



    """Private methods"""


    def __DataFormatting(self, dataToFormat:str|dict):
        if isinstance(dataToFormat, str):
            data = dataToFormat.encode(self.__FORMAT)
            dataLength = len(data)

            formattedData = str(dataLength).encode(self.__FORMAT)
            formattedData += b' ' * (self.__HEADER - len(formattedData))

            return data, formattedData


        elif isinstance(dataToFormat, dict):
            jsonDict = json.dumps(dataToFormat)

            return jsonDict.encode(self.__FORMAT)

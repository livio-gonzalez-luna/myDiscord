import socket, pyaudio, json



class Client:
    def __init__(self):

        '''---------------CLIENT GLOBALS---------------'''

        self.__SERVER = socket.gethostbyname(socket.gethostname())
        self.__PORT = 5050
        self.__HEADER = 1024
        self.__FORMAT = "utf-8"

        self.__client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__client.connect((self.__SERVER, self.__PORT))

        # Initialize PyAudio
        self.__audio = pyaudio.PyAudio()
        self.__STREAM = None

        self.__CHUNK = 1024
        self.__RATE = 44100
        self.__AUDIO_FORMAT = pyaudio.paInt16
        self.__CHANNELS = 2
        




    """Public methods"""


    def ServerQuery(self, type:str, data:dict):    
        if type == "Message":
            self.__MessagePost(data)

        elif type == "Call":
            self.__StartCall()
        
        else:
            self.__SigningIn(type, data)
    



    """Private methods"""


    def __SigningIn(self, mode:str, credentials:dict):
        credentials = {"Type":mode, "Data":credentials}
        credentialsFormatted = json.dumps(credentials).encode(self.__FORMAT)

        self.__client.sendall(credentialsFormatted)
        credentialsResult = self.__client.recv(1024)
        print(credentialsResult)
    


    def __MessagePost(self, msgData:dict):
        userMessage = {"Type":"Message", "Data":msgData}
        messageFormatted = json.dumps(userMessage).encode(self.__FORMAT)

        self.__client.sendall(messageFormatted)
        messageResult = self.__client.recv(1024)
   


    def __Receive(self):
        msgLength = self.__client.recv(self.__HEADER).decode(self.__FORMAT)
        if msgLength:
            msgLength = int(msgLength)
            msg = self.__client.recv(msgLength).decode(self.__FORMAT)
            return msg
        else:
            return None



    def __StartCall(self):
        audioSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        audioSocket.connect((self.__SERVER, self.__PORT + 1))

        dataToSend = {"Type":"Call", "Data":"Start"}
        jsonToSend = json.dumps(dataToSend)

        formattedData, formattedHeader = self.__DataFormatting(jsonToSend)
        fullMessage = formattedHeader + formattedData
        audioSocket.send(fullMessage)

        self.__STREAM = self.__audio.open(format=self.__AUDIO_FORMAT, channels=self.__CHANNELS, rate=self.__RATE, output=True, frames_per_buffer=self.__CHUNK)

        while True:
            data = audioSocket.recv(self.__CHUNK)
            self.__STREAM.write(data)



    def __EndCall(self):
        dataToSend = {"Type":"Call", "Data":"End"}
        jsonToSend = json.dumps(dataToSend)

        formattedData, formattedHeader = self.__DataFormatting(jsonToSend)
        fullMessage = formattedHeader + formattedData
        self.__client.send(fullMessage)

        self.__STREAM.stop_stream()
        self.__STREAM.close()





from DbManager import *
from threading import *
import socket, pyaudio, json, datetime, hashlib, random, string




'''class Channel:
    def __init__(self, server, name):
        self.server = server
        self.name = name
        self.messages = CRUD(DB_CURSOR, f"channel_{name}")
    
    def add_message(self, sender, content):
        # add message to database table
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.messages.Create({"sender": sender, "content": content, "timestamp": timestamp})

    def get_messages(self):
        # retrieve messages from database table
        return self.messages.Read()'''


class Server:
    def __init__(self):

        '''---------------SERVER GLOBALS---------------'''

        self.__IP = socket.gethostbyname(socket.gethostname())
        self.__PORT = 5050
        self.__HEADER = 1024
        self.__FORMAT = "utf-8"
        self.__DISCONNECTION_SIGNAL = "!DISCONNECT"

        self.__server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__server.bind((self.__IP, self.__PORT))

        self.__clients = []
        #self.__channels = [Channel(self, "general"), Channel(self, "random")]


        '''---------------DATABASE GLOBALS---------------'''

        self.__users = CRUD(DB_CURSOR, "user")
        self.__rooms = CRUD(DB_CURSOR, "room")

        #self.__usersColumns = self.__users.GetTableColumns()
        #self.__roomsColumns = self.__rooms.GetTableColumns()
    




    """Public methods"""


    def Run(self):
        self.__server.listen()
        print(f"Server listening on {self.__IP}")

        while True:
            clientSocket, clientIP = self.__server.accept()
            print(f"[{clientIP}]: CONNECTED")

            thread = Thread(target=self.__ThreadedClient, args=(clientSocket, clientIP))
            thread.start()




    """Private methods"""


    def __ThreadedClient(self, socket:socket, ip):
        clientConnected = True

        while clientConnected:
            rawData = socket.recv(self.__HEADER).decode(self.__FORMAT)
            data = rawData.replace("'", "\"")

            clientData = json.loads(data)
            self.__HandlingData(clientData, socket, ip)
            
            
        socket.close()


    """Data Handling"""

    def __HandlingData(self, data:dict, clientSocket:socket, clientIP):
        if data["Type"] == "Message":
            self.__RoomMessages(clientSocket, data)

        elif data["Type"] == "Login":
            self.__LoginCheck(clientSocket, data)
        
        elif data["Type"] == "NewUser":
            self.__NewAccount(clientSocket, data)



    def __RoomMessages(self):
        return None
    


    def __LoginCheck(self, client:socket , credentialToCheck:dict):
        hashedPassword = hashlib.sha256(credentialToCheck["Data"]["Password"].encode()).hexdigest()

        if self.__EncryptionPasswordCheck(hashedPassword):
            #return to the client positive response
            return True
    


    def __NewAccount(self, client:socket, credentialToStore:dict):
        hashedPassword = hashlib.sha256(credentialToStore["Data"]["Password"].encode()).hexdigest()

        if credentialToStore["Username"] == "" or credentialToStore["Password"] == "":
            client.send("Username or password cannot be empty".encode(self.__FORMAT))

        elif credentialToStore["Username"] in self.__users.Read("Username"):
            client.send("Username already exists".encode(self.__FORMAT))
        

        else:
            self.__users[credentialToStore["Username"]] = credentialToStore["Password"]
            response = f"Account created for {credentialToStore['Username']}"
            client.sendall(self.__DataFormatting(response))


    
    def __EncryptionPasswordCheck(self, password:str):
        '''Password salt'''
        # randomChar = string.ascii_letters + "'&é')(-è_çà=~#}{][|`\^@]}¨$£¤*µù%!§:/;.,?"
        
        # def GeneratingSalt():
        #     salt = {}

        #     for i in range(random.randint(5, len(password))):
        #         index = random.randint(0, len(password))
        #         if index in list(salt.keys()):
        #             continue

        #         salt.update({index:random.choice(random.choice(randomChar), "upper", "lower")})

        #     return salt
        

        # def PasswordSalting(unsaltedPassword:str):
        #     saltedPassword = ""
        #     for i in range(len(unsaltedPassword)):
        #         if i in list(encyptionSalt.keys()):
        #             if encyptionSalt[i] == "upper":
        #                 saltedPassword += unsaltedPassword[i].upper()

        #             elif encyptionSalt[i] == "lower":
        #                 saltedPassword += unsaltedPassword[i].lower()

        #             else:
        #                 saltedPassword += encyptionSalt[i]

        #     return saltedPassword


        # encyptionSalt = GeneratingSalt()
        # clientPassword = PasswordSalting(password)
        # clientPassword = hashlib.sha256(clientPassword.encode()).hexdigest()
        # inDatabasePassword = PasswordSalting()
        # inDatabasePassword = hashlib.sha256(inDatabasePassword.encode()).hexdigest()

        '''Password stored in database'''
        inDatabasePassword = None


        if password == inDatabasePassword:
            #store in the database newly salted password
            return True
        
        else:
            return False








        

if __name__ == "__main__":
    server = Server()
    server.Run()





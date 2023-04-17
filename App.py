from Client import *
from threading import *
from tkinter import *
from tkinter import font
from tkinter import ttk
from pathlib import *
from PIL import Image
from datetime import datetime
import customtkinter as ctk

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("dark-blue")


class App(ctk.CTk):
    def __init__(self):
        self.width, self.height = 750, 470
        super().__init__()

        '''---------------TKINTER GLOBALS----------------'''

        #self.geometry(f"{self.width}x{self.height}")
        self.resizable(height=False, width=False)
        self.title("Discord Clone")

        self.__icon = PhotoImage(file = Path("./images-src/discord-logo.png"))
        self.iconphoto(False, self.__icon)

        self.DEFAULT_FONT = ("Microsoft JhengHei UI", 11, "bold")
        #defaultFont = font.nametofont("TkDefaultFont")
        #defaultFont.configure(family="Calibri Light")
        #self.option_add("*Font", defaultFont)

        
        """-----App pages-----"""

        self.__loginPage = LoginPage(self)
        self.__mainPage = MainPage(self)
        self.__loginPage.pack(fill="both", expand=True)
        self.__mainPage.pack(fill="both", expand=True)

        self.__Pages = {"Login":self.__loginPage, "Main":self.__mainPage}
        self.PageSwitch("Login")





    """Public methods"""


    """Switch pages"""
    def PageSwitch(self, nextPage:str, setClient:Client=None):
        self.__RemovePages(nextPage)
        activePage = self.__Pages[nextPage]

        if nextPage == "Main":
            self.width, self.height = int(self.width*1.5), int(self.height*1.5)
            self.geometry(f"{self.width}x{self.height}")
            activePage.SetAppClient(setClient)
            self.__mainPage.pack(fill="both", expand=True)
            activePage.Main()

        elif nextPage == "Login":
            self.width, self.height = 750, 470
            self.geometry(f"{self.width}x{self.height}")
            self.__loginPage.pack(fill="both", expand=True)
            activePage.Login()

        activePage.tkraise()




    """Private methods"""


    def __RemovePages(self, activePage:str):
        for page in self.__Pages:
            if page != activePage:
                self.__Pages[page].forget()
    














"""Defines the Login page"""

class LoginPage(ctk.CTkFrame):
    def __init__(self, controller:App):
        super().__init__(controller)
        self.__APP = controller

        loginBG = ctk.CTkImage(Image.open(Path("./images-src/loginBG-myDiscord.png")), size=(self.__APP.width, self.__APP.height))
        BG = titleImg = ctk.CTkLabel(self, text="", image=loginBG)
        BG.grid(row=0, column=0)


        self.__loginFrame = ctk.CTkFrame(self, width=400, height=350)
        self.__loginFrame.grid(row=0, column=0, sticky="ns")

        logo = ctk.CTkImage(Image.open(Path("./images-src/discord-logo.png")), size=(95, 65))
        titleImg = ctk.CTkLabel(self.__loginFrame, text="", image=logo)
        titleImg.pack(pady=40)
    





    """Public methods"""


    def Login(self):        
        self.__appClient = Client()
        self.__LoginBox()





    """Private methods"""

    def __LoginBox(self):
        self.__loginCheck = False


        """-----Signing Window-----"""
        self.__loginBox = ctk.CTkTabview(self.__loginFrame, width=200, height=150)
        self.__loginBox.pack(padx=15, pady=(0, 50))

        self.__loginBox.add("Login")
        self.__loginBox.add("New Account")


        loginEntries = {
            "Username":ctk.CTkEntry(self.__loginBox.tab("Login"), justify=CENTER, placeholder_text="Username/Email", font=self.__APP.DEFAULT_FONT), 
            "Password":ctk.CTkEntry(self.__loginBox.tab("Login"), justify=CENTER, placeholder_text="Password", font=self.__APP.DEFAULT_FONT, show=f"•")}
        newUserEntries = {
            "Username":ctk.CTkEntry(self.__loginBox.tab("New Account")),
            "First Name":ctk.CTkEntry(self.__loginBox.tab("New Account")),
            "Last Name":ctk.CTkEntry(self.__loginBox.tab("New Account")),
            "Email":ctk.CTkEntry(self.__loginBox.tab("New Account")),
            "Create Password":ctk.CTkEntry(self.__loginBox.tab("New Account"), show=f"•")}

        for entry in loginEntries:
            loginEntries[entry].pack(fill="x", padx=10, pady=5, anchor="center")

        for entry in newUserEntries:
            newUserEntries[entry].configure(justify=CENTER, placeholder_text=entry, font=self.__APP.DEFAULT_FONT)
            newUserEntries[entry].pack(fill="x", padx=10, pady=5, anchor="center")


        loginButton = ctk.CTkButton(self.__loginBox.tab("Login"), text="Login", font=self.__APP.DEFAULT_FONT, command=lambda: self.__CredentialCheck((loginEntries["Username"].get(), loginEntries["Password"].get()), "Login"))
        signingButton = ctk.CTkButton(self.__loginBox.tab("New Account"), text="Sign Up", font=self.__APP.DEFAULT_FONT, command=lambda: self.__CredentialCheck((newUserEntries["Username"].get(), newUserEntries["First Name"].get(), newUserEntries["Last Name"].get(), newUserEntries["Email"].get(), newUserEntries["Create Password"].get()), "NewUser"))
        loginButton.pack(pady=20, anchor="center")
        signingButton.pack(pady=20, anchor="center")


        """-----Server message-----"""
        self.__serverMessage = ctk.CTkLabel(self.__loginFrame, text="", wraplength=200)
        self.__serverMessage.pack(pady=20, anchor="center")



    def __CredentialCheck(self, credentials:tuple, mode:str):
        self.__loginCheck = True
        print(self.__loginCheck)
        if self.__loginCheck:
            #self.__serverMessage.configure(text_color="#ff0000", text="Error")
            self.__APP.PageSwitch("Main", self.__appClient)
        '''if mode == "Login":
            userCredentials = {"Username":credentials[0], "Password":credentials[1]}
            self.__loginCheck = self.__appClient.ServerQuery(mode, userCredentials)

        else:
            newCredentials = {"Username":credentials[0], "First Name":credentials[1], "Last Name":credentials[2], "Email":credentials[3], "Password":credentials[4]}
            self.__loginCheck = self.__appClient.ServerQuery(mode, newCredentials)'''










"""Defines the Main page"""

class MainPage(ctk.CTkFrame):
    def __init__(self, controller:App, client:Client=None):
        super().__init__(controller)

        self.__APP = controller
        self.__client = client





    """---------------Public methods---------------"""


    """Sets the current client"""
    def SetAppClient(self, client:Client):
        self.__client = client
    


    def Main(self):
        self.__channelsWidth, self.__roomsWidth, self.__messagesWidth, self.__usersWidth = int(self.__APP.width * 0.1), int(self.__APP.width * 0.15), \
            int(self.__APP.width * 0.7), int(self.__APP.width * 0.15)
        
        self.__listeningThread = Thread(target=self.__ThreadedListener)
        self.__listeningThread.daemon = True
        self.__listeningThread.start()
        

        '''Simulating userData'''

        self.__userData = {
            "User":{"ID":0, "Username":"Burger"},
            "Servers":{
                "Friends":[2, 5, 6],
                "GigaBoys":{
                    "ServerID":1,
                    "Users":[2, 5, 6],
                    "Rooms":[3, 5]
                },
                "Gamers":{
                    "ServerID":2,
                    "Users":[2, 5, 6],
                    "Rooms":[4, 8]
                }
            }
        }

        self.__friends = {
            2:"Burger",
            5:"Chilling",
            6:"BAMBOULA"
        }
        self.__rooms = {
            3:"Chad",
            5:"Rizz",
            4:"TryHard",
            8:"Casual"
        }

        self.__currentChannelRooms = []
        self.__userChannels = list(self.__userData["Servers"].keys())


        self.__ChannelSelection()
        self.__RoomSelection()
        self.__RoomMessages()





    """---------------Private methods---------------"""


    def __ChannelSelection(self):
        self.__channelFrame = ctk.CTkScrollableFrame(self, corner_radius=0, width=self.__channelsWidth, height=self.__APP.height)
        self.__channelFrame.grid(row=0, column=0, sticky="nsew")
        self.__channelFrame.grid_rowconfigure(4, weight=1)

        self.__UserServers()



    def __RoomSelection(self):
        self.__roomsChannelFrame = ctk.CTkFrame(self, corner_radius=0, width=self.__roomsWidth, height=self.__APP.height)
        self.__roomsChannelFrame.grid(row=0, column=1, sticky="nsew")
        #self.__roomsChannelFrame.grid_rowconfigure(4, weight=1)
        topServer = self.__userChannels[1]

        self.__UserServerRooms(topServer, self.__userData["Servers"][topServer]["Rooms"])
    


    def __RoomMessages(self):
        self.__chatroomFrame = ctk.CTkFrame(self, corner_radius=0, width=self.__messagesWidth, height=self.__APP.height)
        self.__chatroomFrame.grid(row=0, column=2, sticky="nsew")




    """----------Frames elements----------"""

    def __UserServers(self):
        self.__serverButtons = []
        logo = ctk.CTkImage(Image.open(Path("./images-src/social-networks.png")), size=(15, 13))
        friendsLogo = ctk.CTkImage(Image.open(Path("./images-src/bavarder.png")), size=(19, 17))


        for i in range(len(self.__userChannels)):
            if self.__userChannels[i] == "Friends":
                privateButton = ctk.CTkButton(self.__channelFrame, corner_radius=0, width=self.__channelsWidth, height=40, border_spacing=10, text=self.__userChannels[i], image=friendsLogo, 
                    fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), anchor="w", command=lambda x=i: self.__UserServerRooms(self.__userChannels[x], self.__userData["Servers"][self.__userChannels[x]])) 
                privateButton.grid(row=1, column=0, sticky="ew")
                self.__serverButtons.append(privateButton)

            else:
                button = ctk.CTkButton(self.__channelFrame, corner_radius=0, width=self.__channelsWidth, height=40, border_spacing=10, text=self.__userChannels[i], image=logo, 
                    fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), anchor="w", command=lambda x=i: self.__UserServerRooms(self.__userChannels[x], self.__userData["Servers"][self.__userChannels[x]]["Rooms"]))
                button.grid(row=i + 2, column=0, sticky="ew")
                self.__serverButtons.append(button)



    def __UserServerRooms(self, channel:str, rooms:list):
        self.__currentChannel = channel
        channelLabel = ctk.CTkLabel(self.__roomsChannelFrame, text=f"{self.__currentChannel}", height=30)
        channelLabel.grid(row=0, column=0, sticky=EW)
        channelRooms = ctk.CTkScrollableFrame(self.__roomsChannelFrame, corner_radius=0, width=self.__roomsWidth, height=self.__APP.height - 80)
        channelRooms.grid(row=1, column=0, sticky=NSEW)

        self.__ChannelRoomsQuery()
        self.__CleanUpRoomButtons()
        i = 0


        '''if channel == "Friends":
            self.__RoomSwitch(self.__userData["Servers"][self.__currentChannel][i], self.__friends[i])
        else:
            self.__RoomSwitch(self.__userData["Servers"][self.__currentChannel]["Rooms"][i], self.__rooms[i])'''
        
        for id in rooms:
            if channel == "Friends":
                friendsButton = ctk.CTkButton(channelRooms, corner_radius=0, width=self.__roomsWidth, height=40, border_spacing=10, text=self.__friends[id],
                    fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), anchor="w", command=lambda x=id: self.__RoomSwitch(self.__friends[x], x))
                friendsButton.grid(row=i + 2, column=0, sticky="ew")
                self.__currentChannelRooms.append(friendsButton)
                i += 1

            else:
                button = ctk.CTkButton(channelRooms, corner_radius=0, width=self.__roomsWidth, height=40, border_spacing=10, text=self.__rooms[id],
                    fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), anchor="w", command=lambda x=id: self.__RoomSwitch(self.__rooms[x], x))
                button.grid(row=i + 2, column=0, sticky=EW)
                self.__currentChannelRooms.append(button)
                i += 1

        logo = ctk.CTkImage(Image.open(Path("./images-src/lamouche-min.png")), size=(38, 30))
        self.__userSettings = ctk.CTkButton(self.__roomsChannelFrame, corner_radius=10, width=self.__roomsWidth, border_spacing=10, text="Burger",
            image=logo, compound="left", fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), anchor="w", command=None)
        self.__userSettings.grid(row=2, column=0, sticky=NSEW)



    def __ChatFrame(self):
        self.__chatDisplayOptions = ctk.CTkLabel(self.__chatroomFrame, corner_radius=0, text=f"{self.__currentRoom}", width=self.__messagesWidth, height=30, anchor="w")
        self.__chatDisplayOptions.grid(row=0, column=0, columnspan=2, sticky=E, padx=25)
        self.__sidePanelToggle = ctk.CTkSwitch(self.__chatroomFrame, text="Display Users", command=self.__DisplaySidePanel)
        self.__sidePanelToggle.grid(row=0, column=1)

        self.__chatFrame = ctk.CTkScrollableFrame(self.__chatroomFrame, corner_radius=0, width=self.__messagesWidth, height=self.__APP.height - 80)
        self.__chatFrame.grid(row=1, column=0, columnspan=2, sticky=W)

        self.__message = ctk.CTkEntry(self.__chatroomFrame, placeholder_text="Message", width=int(self.__APP.width * 0.55))
        self.__message.grid(row=2, column=0, padx=(20, 0), pady=10, sticky=W)
        send = ctk.CTkImage(Image.open(Path("./images-src/paper-aeroplane.png")), size=(20, 20))
        self.__sendButton = ctk.CTkButton(self.__chatroomFrame, width=110, image=send, text="Send", fg_color="transparent", text_color=("gray10", "#DCE4EE"), command=lambda: self.__NewMessage(self.__message.get(), self.__userData["User"]["Username"], self.__currentRoomId))
        self.__sendButton.grid(row=2, column=1, padx=(0, 20), pady=10, sticky=W)
        self.__sendButton.bind("<Return>", (lambda: self.__NewMessage(self.__message.get(), self.__userData["User"]["Username"], self.__currentRoomId)))


        if self.__currentChannel == "Friends":
            self.__sidePanelLabel = ctk.CTkLabel(self.__chatroomFrame, corner_radius=0, text=f"Users", height=30, anchor="w")
            self.__sidePanelLabel.grid(row=0, column=2, sticky=W, padx=25)
            self.__sidePanel = ctk.CTkFrame(self.__chatroomFrame, corner_radius=0, width=100, height=self.__APP.height - 80)
            self.__sidePanel.grid(row=1, column=2, rowspan=2, sticky=EW)
        else:
            self.__sidePanelLabel = ctk.CTkLabel(self.__chatroomFrame, corner_radius=0, text=f"{self.__currentChannel} users", height=30, anchor="w")
            self.__sidePanelLabel.grid(row=0, column=2, sticky=W, padx=25)
            self.__sidePanel = ctk.CTkScrollableFrame(self.__chatroomFrame, corner_radius=0, width=100, height=self.__APP.height - 80)
            self.__sidePanel.grid(row=1, column=2, rowspan=2, sticky=EW)

        self.__sidePanelLabel.grid_remove()
        self.__sidePanel.grid_remove()




    """----------Button Actions----------"""

    def __RoomSwitch(self, room:str, roomId:int):
        self.__currentRoom, self.__currentRoomId = room, roomId
        #print(self.__currentChannel, self.__currentRoom, self.__currentRoomId)

        self.__RoomMessagesQuery()
        self.__ChatFrame()



    def __NewMessage(self, message:str, user:str, room:int):
        if message and room == self.__currentRoomId:
            timestamp = datetime.now().strftime(f"%m/%d/%Y, %H:%M")
            messageFrame = ctk.CTkFrame(self.__chatFrame, width=self.__messagesWidth)
            messageFrame.grid(padx=10, pady=(0, 25))

            logo = ctk.CTkImage(Image.open(Path("./images-src/lamouche-min.png")), size=(50, 42))
            user = ctk.CTkButton(messageFrame, text=user, image=logo, compound="left", text_color="#FF3333", hover_color=("gray70", "gray30"), fg_color="transparent", anchor="w")
            postTimestamp = ctk.CTkLabel(messageFrame, text=timestamp, font=("Microsoft JhengHei UI", 10), justify=LEFT, anchor="w")
            user.grid(row=0, column=0, sticky=W)
            postTimestamp.grid(row=0, column=1, sticky=W)

            userPost = ctk.CTkLabel(messageFrame, text=message, width=self.__messagesWidth, justify=LEFT, anchor="w", wraplength=self.__messagesWidth - 10)
            userPost.grid(row=1, column=0, columnspan=2, sticky=W)
            self.__message.delete(0, END)


            if user == self.__userData["User"]["Username"]:
                '''messageData = {"Data":message, "TimeStamp":timestamp, "UserID":self.__userData["ID"], "RoomID":self.__currentRoomId}
                self.__client.ServerQuery("Message", messageData)'''



    def __DisplaySidePanel(self):
        if self.__sidePanelToggle.get() == 1:
            self.__chatFrame.configure(width = self.__messagesWidth - 100)
            self.__sidePanelLabel.grid()
            self.__sidePanel.grid()

            if self.__currentChannel == "Friends":
                self.__sidePanelToggle.configure(text=f"{self.__currentRoom} details")
                self.__sidePanelLabel.configure(text=f"{self.__currentRoom}")
            else:
                self.__sidePanelToggle.configure(text=f"Display Users")
                self.__ChannelUsers()
        

        elif self.__sidePanelToggle.get() == 0:
            self.__chatFrame.configure(width = self.__messagesWidth)
            self.__sidePanelLabel.grid_remove()
            self.__sidePanel.grid_remove()




    """----------Server Related Methods----------"""

    def __Disconnect(self):
        return None
    


    def __ChannelRoomsQuery(self):
        return None


    
    def __RoomMessagesQuery(self):
        return None
    


    def __ThreadedListener(self):
        while True:
            if self.__client.ServerListener():
                self.__NewMessage("BRO", "Burger", 0)
    
    


    """----------Utility----------"""

    def __CleanUpRoomButtons(self):
        if self.__currentChannelRooms != []:
            for room in self.__currentChannelRooms:
                room.grid_forget()

            self.__currentChannelRooms = []



    def __ChannelUsers(self):
        i = 0
        for user in self.__userData["Servers"][self.__currentChannel]["Users"]:
            serverUserButton = ctk.CTkButton(self.__sidePanel, corner_radius=0, width=self.__usersWidth, height=40, border_spacing=10, text=f"User {user}",
                fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), anchor="w", command=None)
            serverUserButton.grid(row=i + 2, column=0, sticky=E)
            i += 1
        
    

    def __RoomUsers(self):
        return None
    








    class Settings(ctk.CTkFrame):
        def __init__(self, controller:App, currentClient:Client):
            MainPage.__APP
            














if __name__ == "__main__":
    discordClone = App()
    discordClone.mainloop()





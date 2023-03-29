from Client import *
from tkinter import *
from tkinter import font
from pathlib import *
from PIL import Image
import customtkinter as ctk

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("dark-blue")


class App(ctk.CTk):
    def __init__(self):
        self.width, self.height = 750, 500
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
            self.geometry(f"{int(self.width*1.5)}x{int(self.height*1.5)}")
            activePage.SetAppClient(setClient)
            activePage.Main()

        else:
            self.geometry(f"{self.width}x{self.height}")
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
        #self.__appClient.MessagePost("!DISCONNECT")
        self.__LoginBox()
        
        if self.__loginCheck:
            self.__APP.PageSwitch("Main", self.__appClient)





    """Private methods"""

    def __LoginBox(self):
        self.__loginCheck = False

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



    def __CredentialCheck(self, credentials:tuple, mode:str):
        if mode == "Login":
            userCredentials = {"Username":credentials[0], "Password":credentials[1]}
            self.__loginCheck = self.__appClient.ServerQuery(mode, userCredentials)

        else:
            newCredentials = {"Username":credentials[0], "First Name":credentials[1], "Last Name":credentials[2], "Email":credentials[3], "Password":credentials[4]}
            self.__loginCheck = self.__appClient.ServerQuery(mode, newCredentials)










"""Defines the Main page"""

class MainPage(ctk.CTkFrame):
    def __init__(self, controller:App, client:Client=None):
        super().__init__(controller)

        self.__APP = controller
        self.__client = client





    """Public methods"""


    """Sets the current client"""
    def SetAppClient(self, client:Client):
        self.__client = client
    
    def Main(self):
        self.__ServerSelection()
        self.__RoomSelection()
        self.__RoomMessages()




    """Private methods"""


    def __ServerSelection(self):
        self.__serversFrame = ctk.CTkFrame(self, corner_radius=0)
        self.__serversFrame.grid(row=0, column=0, sticky="nsew")
        self.__serversFrame.grid_rowconfigure(1, weight=1)
        self.navigation_frame_label = ctk.CTkLabel(self.__serversFrame, text="  Create server", compound="left", font=ctk.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

    def __RoomSelection(self):
        self.__roomsServerFrame = ctk.CTkFrame(self, corner_radius=0).grid(row=0, column=1, sticky="nsew")
    
    def __RoomMessages(self):
        self.__messagesFrame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.__messagesFrame.grid(row=0, column=2, sticky="nsew")
        self.__messagesFrame.grid_columnconfigure(0, weight=1)

        frameLabel = ctk.CTkLabel(self.__messagesFrame, text="MESSAGE FRAME")
        frameLabel.grid(row=0, column=1)
    


    """Connection handling"""

    def __Disconnect(self):
        self.__client.MessagePost("!DISCONNECT")
        self.__APP.PageSwitch("Login")
    








if __name__ == "__main__":
    discordClone = App()
    discordClone.mainloop()





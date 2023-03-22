from Client import *
from tkinter import *
import customtkinter as ctk



ctk.set_appearance_mode("System")
ctk.set_default_color_theme("dark-blue")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        '''---------------TKINTER GLOBALS----------------'''

        self.geometry("600x500")
        self.title("Discord Clone")

        self.__icon = PhotoImage(file = "images-src\discord-logo.png")
        self.iconphoto(False, self.__icon)

        
        """-----App pages-----"""

        self.__loginPage = LoginPage(self)
        self.__mainPage = MainPage(self) 

        self.__Pages = {"Login":self.__loginPage, "Main":self.__mainPage}
        self.PageSwitch("Login")

    


    """Public methods"""


    """Switch pages"""
    def PageSwitch(self, nextPage:str, setClient:Client=None):
        activePage = self.__Pages[nextPage]
        if nextPage == "Main":
            activePage.SetAppClient(setClient)

        activePage.tkraise()
    













"""Defines the Login page"""

class LoginPage(Frame):
    def __init__(self, controller:App):
        self.__APP = controller
    



    """Private methods"""


    def __Login(self):

        def CheckCredential():
            return None
        

        self.__LoginBox()
        self.__client = Client()
        loginChecked = False

        self.__client.Post("Bro")
        self.__client.ClientLogin()
        

        if loginChecked:
            self.__APP.PageSwitch("Main", self.__client)



    """Elements on Login page"""

    def __LoginBox(self):
        return None
    








"""Defines the Main page"""

class MainPage(Frame):
    def __init__(self, controller:App, client:Client):
        self.__APP = controller
        self.__client = client




    """Public methods"""

    """Sets the current client"""
    def SetAppClient(self, client:Client):
        self.__client = client
    



    """Private methods"""


    def __Main(self):
        self.__RoomSelection()
        self.__RoomMessages()


    
    """Elements on Main page"""

    def __RoomSelection(self):
        return None
    


    def __RoomMessages(self):
        return None
    


    """Connection handlers"""


    def __Disconnect(self):
        self.__client.Post("DISCONNECT")
        self.__APP.PageSwitch("Login")
    



















if __name__ == "__main__":
    discordClone = App()
    discordClone.mainloop()
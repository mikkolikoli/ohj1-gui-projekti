"""
This is a banking program with different account functionality.
For the management of the users I have made a class named "Userdatabase". Its data structure is
After logging in, you'll have the possibility to deposit money to your account, transfer money from your account to
another account or withdraw money
"""

from tkinter import *
from tkinter.ttk import *


class Ui:
    """

    """

    def __init__(self):
        """

        """

        self._window = Tk()
        self.__database = UserDatabase

    def start(self):
        """
        starts the program
        :return:
        """

        login_ui = RegisterUi()
        self._window.mainloop()

    def quit(self):
        """
        Quits the program
        :return:
        """

        self._window.destroy()

    def show_error_popup(self, error_text):
        """
        Shows an error popup
        :param error_text: str, the error text
        """
        # TODO: implement method
        pass


class LoginUi(Ui):
    """
    A class managing the login function of the
    """

    def __init__(self):
        """
        Constructor. Creates the login ui
        """

        super().__init__()

        # showing the screen on which all the widgets will be placed on

        self.__screen = Frame(self._window)
        self.__screen.grid(row=0, column=0, sticky="nsew")

        # labels

        self.__header = Label(self.__screen, text="Login")
        self.__username_label = Label(self.__screen, text="Username")
        self.__password_label = Label(self.__screen, text="Password")
        self.__error_label = Label(self.__screen)
        self.__register_label = Label(self.__screen, text="Don't have an account yet?")

        # entries

        self.__username_entry = Entry(self.__screen)
        self.__password_entry = Entry(self.__screen, show="*")

        # buttons

        self.__login_button = Button(self.__screen, text="Login", command=self.login)
        self.__register_button = Button(self.__screen, text="Create an account", command=self.register)
        self.__quit_button = Button(self.__screen, text="Quit", command=self.quit)

        # placing the widgets

        self.__header.pack()
        self.__username_label.pack()
        self.__username_entry.pack()
        self.__password_label.pack()
        self.__password_entry.pack()

        self.__login_button.pack()
        self.__register_label.pack()
        self.__register_button.pack()

        self.__quit_button.pack(side=RIGHT)

    def login(self):
        """
        A method to check the login credentials and open the main ui if the credentials are correct
        """

        username = self.__username_entry.get()
        password = self.__password_entry.get()

        if self.__database.check_user(username, password, password):
            main_ui = MainUi(self.__database.get_user(username, username))

        else:
            self.__error_label["text"] = "Please check your credentials"

    def register(self):
        """
        A method to switch to the register screen
        :return:
        """
        self.__screen.grid_remove()
        register = RegisterUi()


class RegisterUi(Ui):
    """
    The register ui
    """

    def __init__(self):
        """
        Constructor
        """

        super().__init__()

        # initializing the frame on which the widgets are placed

        self.__screen = Frame(self._window)
        self.__screen.grid(row=0, column=0, sticky="nsew")

        # creating a StringVar for updates to the password_security progressbar on each update on the password entry

        self.password = StringVar(self.__screen)
        self.password.trace("w", self.strength)

        # labels

        self.__header = Label(self.__screen, text="Register")
        self.__username_label = Label(self.__screen, text="Username")
        self.__password_label = Label(self.__screen, text="Password")
        self.__repeat_password_label = Label(self.__screen, text="Repeat password")
        self.__password_security_label = Label(self.__screen, text="Password strength: Weak")
        self.__login_label = Label(self.__screen, text="Already got an account? Log in instead")
        self.__error_label = Label(self.__screen)

        # entry fields

        self.__username_entry = Entry(self.__screen)
        self.__password_entry = Entry(self.__screen, textvariable=self.password, show="*")
        self.__repeat_password_entry = Entry(self.__screen, show="*")

        # buttons

        self.__register_button = Button(self.__screen, text="Register", command=self.register)
        self.__login_button = Button(self.__screen, text="Login", command=self.to_login)
        self.__quit_button = Button(self.__screen, text="Quit", command=self.quit)

        # progressbar

        self.__password_security = Progressbar(self.__screen, orient=HORIZONTAL, length=100, mode="determinate")

        # placing the widgets

        self.__header.grid(row=0, column=1)

        self.__username_label.grid(row=1, column=0)
        self.__username_entry.grid(row=1, column=1)
        self.__password_label.grid(row=2, column=0)
        self.__password_entry.grid(row=2, column=1)
        self.__repeat_password_label.grid(row=3, column=0)
        self.__repeat_password_entry.grid(row=3, column=1)

        self.__error_label.grid(row=4, column=1)

        self.__password_security_label.grid(row=5, column=1)
        self.__password_security.grid(row=6, column=1)
        self.__register_button.grid(row=7, column=1)

        self.__login_label.grid(row=8, column=1)
        self.__login_button.grid(row=9, column=1)

        self.__quit_button.grid(row=10, column=2)

    def test(self):
        """
        please fucking work you piece of shit code
        :return:
        """

        print(self.password.get())

    def register(self):
        """
        Gets the entries from the user, checks if they are not empty, the two passwords match and creates an account
        """

        username = self.__username_entry.get()
        password = self.password
        repeat = self.__repeat_password_entry.get()

        # checks if the fields are not empty and the passwords match

        if username != "" and password != "" and (password == repeat):
            self.__database.add_user(username, password, password)

        elif password != repeat:
            self.__error_label["text"] = "Passwords don't match"

        else:
            self.__error_label["text"] = "Please fill out all the fields"

    def to_login(self):
        """
        Changes the current screen to the login screen
        """

        self.__screen.grid_remove()
        login_ui = LoginUi()

    def strength(self, *args):
        """
        A method to show the strength of the password entered by the user in the progressbar and the label for the
        password strength
        :param args: fix for an error I had with the self.__password.trace() command
        """

        password = self.password.get()

        if 0 <= len(password) <= 8:
            self.__password_security["value"] = 0
            self.__password_security_label["text"] = "Password strength: Weak"

        elif 8 < len(password) <= 12:
            self.__password_security["value"] = 50
            self.__password_security_label["text"] = "Password strength: Medium"

            if any(char.isdigit() for char in password):
                self.__password_security["value"] = 100
                self.__password_security_label["text"] = "Password strength: Strong"

        else:
            self.__password_security["value"] = 100

            self.__password_security_label["text"] = "Password strength: Strong"


class MainUi(Ui):
    """
    The main ui
    """

    def __init__(self, current_user):
        """
        Constructor for the main ui
        :param current_user: Account, the user that's currently logged in
        """

        super().__init__()

        self.__user = current_user

        # TODO: create UI


class Account:
    """
    this class manages the individual accounts
    """

    def __init__(self, username, admin=False):
        """
        Constructor of the class Account.
        :param username: string, the username of the account
        :param admin: bool, is the user an admin? Default is False
        """

        self.__username = username
        self.__admin = admin
        self.__balance = 0.0
        self.__log = []

    def __str__(self):
        """
        returns the Accounts username
        :return: str, the username
        """

        return self.__username

    def add_money(self, money):
        """
        This method adds money to the account's balance
        :param money: float, the amount of money to be added
        :return: False if the user tries to deposit a negative amount of money
        """

        if money < 0:
            return False

        self.__balance += money

    def remove_money(self, money):
        """
        This method removes money from the account's balance
        :param money: float, the amount of money to be removed
        :return: False if the action fails
        """

        if money < 0:
            return False

        elif self.__balance - money < 0:
            return False

        else:
            self.__balance -= money

    def transfer(self, other_account, money):
        """
        This method transfers money to another account and adds it to the log
        :param other_account: Account, the account the money is getting transferred to
        :param money: float, the amount of money to be
        :return: str, the error type if something goes wrong
        """

        if money <= 0:
            return "negative"

        elif self.__balance - money < 0:
            return "no balance"

        else:
            other_account.add_money(money)
            self.remove_money(money)

    def add_to_log(self, action):
        """
        Adds something to the log. Is used in in the MainUi class after each action
        :param action: str, the action that should be added to the log.
        The format needs to be: change on the balance;action description
        """

        change, description = action.split(";")
        log_entry = f"{change}: {description}"

        self.__log.append(log_entry)

    def get_log(self):
        """
        Returns the log. Is used in the MainUi class to display the users log
        :return: str, the log as a string with an empty row between each entry
        """

        log = "\n\n".join(self.__log)

        return log

    def get_balance(self):
        """
        returns the accounts balance
        :return: float, the balance
        """

        return self.__balance

    def is_admin(self):
        """
        returns whether the user is an admin
        :return:
        """

        return self.__admin


class UserDatabase:
    """
    saves all the user data
    """

    def __init__(self):
        """
        Constructor. Database is a dict
        """

        self.__database = {}

    def add_user(self, username, password):
        """
        adds the user to the database
        :param username: str, the username
        :param password: str, the password
        """

        user = Account(username, password)
        self.__database[username] = {"user": user, "password": password}

    def check_user(self, username, password):
        """
        checks if the username and password are correct
        :param username: str, the username
        :param password: str, the password
        :return: bool, are the username and password correct
        """

        if username in self.__database and self.__database[username]["password"] == password:
            return True

        else:
            return False

    def get_user(self, username):
        """
        Returns the user saved in the database with the username as the key
        :param username: str, the user to be returned
        :return: Account, the user with the correct username
                False, if the user doesn't exist
        """

        if username in self.__database:
            return self.__database[username]["user"]

        else:
            return False


def main():

    ui = Ui()
    ui.start()


if __name__ == "__main__":
    main()

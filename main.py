""""
This is a banking program with different account functionality.
For the management of the users I have made a class named "Userdatabase". Its data structure is
After logging in, you'll have the possibility to deposit money to your account, transfer money from your account to
another account or withdraw money
"""
import tkinter.messagebox
from tkinter import *
from tkinter.ttk import *


# TODO: rethink if all attributes need to be private
# TODO: add comments
# TODO: fix withdraw bug


class App(Tk):
    """

    """

    def __init__(self):
        """

        """

        super().__init__()
        self.database = UserDatabase()
        self.login_frame = LoginFrame(self)
        self.register_frame = RegisterFrame(self)
        self.main_frame = None

        self.title = "Banking program"

        self.currently_open_frame = self.login_frame

        self.login_frame.pack()

    def start(self):
        """
        starts the program
        :return:
        """

        self.mainloop()

    def close(self):
        """
        closes the program
        :return:
        """

        self.destroy()

    def login(self, username, password):
        """
        A method for the login process
        :param username: str, the username
        :param password: str, the password
        :return:
        """

        if self.database.check_credentials(username, password):
            self.main_frame = MainUiFrame(self.database.get_user(username), self.database, self)
            self.login_frame.reset_fields()
            self.login_frame.pack_forget()
            self.main_frame.pack()

            self.currently_open_frame = self.main_frame

        else:
            self.login_frame.show_error_message("Please check your credentials")

    def register(self, username, password, repeat):
        """
        A method for the register process
        :param username: str, the username
        :param password: str, the password
        :param repeat: str, the repeated password
        :return:
        """

        # checks if the fields are not empty and the passwords match

        if username != "" and password != "" and password == repeat and username not in self.database:
            self.database.add_user(username, password)
            tkinter.messagebox.showinfo(title="Congrats", message="You have successfully created an account")
            self.open_login_frame()

        elif password != repeat:
            self.register_frame.show_error_message("The passwords don't match")

        elif username in self.database:
            self.register_frame.show_error_message("A user with the same username already exists. "
                                                   "Please use another one")

        else:
            self.register_frame.show_error_message("Please fill out all the fields")

    def open_register_frame(self):
        """
        A method to open the register frame
        :return:
        """

        self.login_frame.reset_fields()

        self.login_frame.pack_forget()
        self.register_frame.pack()

        self.currently_open_frame = self.register_frame

    def open_login_frame(self):
        """
        A method to close the currently open frame and open the login frame
        :return:
        """

        if self.currently_open_frame == self.register_frame:
            self.currently_open_frame.reset_fields()

        self.currently_open_frame.pack_forget()
        self.login_frame.pack()

        self.currently_open_frame = self.login_frame


class LoginFrame(Frame):
    """
    A class managing the login function of the
    """

    def __init__(self, root=None):
        """
        Constructor for
        :param root:
        """

        super().__init__(root)

        # labels

        self.__header = Label(self, text="Login")
        self.__username_label = Label(self, text="Username")
        self.__password_label = Label(self, text="Password")
        self.__error_label = Label(self)
        self.__register_label = Label(self, text="Don't have an account yet?")

        # entries

        self.__username = StringVar(self)
        self.__password = StringVar(self)
        self.__username_entry = Entry(self, textvariable=self.__username)
        self.__password_entry = Entry(self, textvariable=self.__password, show="*")

        # buttons

        self.__login_button = Button(self, text="Login", command=lambda: root.login(self.__username.get(),
                                                                                    self.__password.get()))
        self.__register_button = Button(self, text="Create an account", command=lambda: root.open_register_frame())
        self.__quit_button = Button(self, text="Quit", command=lambda: root.close())

        # placing the widgets

        self.__header.grid(row=0, column=0, columnspan=3)

        self.__username_label.grid(row=1, column=0)
        self.__username_entry.grid(row=1, column=1)
        self.__password_label.grid(row=2, column=0)
        self.__password_entry.grid(row=2, column=1)

        self.__error_label.grid(row=3, column=1)

        self.__login_button.grid(row=4, column=1)
        self.__register_label.grid(row=5, column=1)
        self.__register_button.grid(row=6, column=1)

        self.__quit_button.grid(row=7, column=2)

    def show_error_message(self, text):
        """
        shows an error message
        :param text: str, the error message
        :return:
        """

        self.__error_label["text"] = text
        self.reset_fields()

    def reset_fields(self):
        """
        clears the entry fields
        :return:
        """

        self.__username.set("")
        self.__password.set("")


class RegisterFrame(Frame):
    """
    The register ui
    """

    def __init__(self, root=None):
        """
        Constructor
        """

        super().__init__(root)

        # creating a StringVar for updates to the password_security progressbar on each update on the password entry

        self.username = StringVar(self)
        self.password = StringVar(self)
        self.repeat_password = StringVar(self)
        self.password.trace("w", self.strength)

        # labels

        self.__header = Label(self, text="Register")
        self.__username_label = Label(self, text="Username")
        self.__password_label = Label(self, text="Password")
        self.__repeat_password_label = Label(self, text="Repeat password")
        self.__password_security_label = Label(self, text="Password strength: Weak")
        self.__login_label = Label(self, text="Already got an account? Log in instead")
        self.__error_label = Label(self)

        # entry fields

        self.__username_entry = Entry(self, textvariable=self.username)
        self.__password_entry = Entry(self, textvariable=self.password, show="*")
        self.__repeat_password_entry = Entry(self, textvariable=self.repeat_password, show="*")

        # buttons

        self.__register_button = Button(self, text="Register",
                                        command=lambda: root.register(self.username.get(), self.password.get(),
                                                                      self.repeat_password.get()))
        self.__login_button = Button(self, text="Login", command=lambda: root.open_login_frame())
        self.__quit_button = Button(self, text="Quit", command=lambda: root.close())

        # progressbar

        self.__password_security = Progressbar(self, orient=HORIZONTAL, length=100, mode="determinate")

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

    def show_error_message(self, text):
        """
        shows an error message
        :param text: str, the error message
        :return:
        """

        self.__error_label["text"] = text
        self.reset_fields()

    def reset_fields(self):
        """
        clears the entry fields
        :return:
        """

        self.username.set("")
        self.password.set("")
        self.repeat_password.set("")

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


class MainUiFrame(Frame):
    """
    The main ui
    """

    def __init__(self, current_user, database, root=None):
        """
        Constructor for the main ui
        :param current_user: Account, the user that's currently logged in
        :param database:
        :param root:
        """

        super().__init__(root)

        self.user = current_user
        self.database = database

        # balance StringVar

        self.balance = StringVar(root)
        self.balance.set(self.user.balance)

        # label

        self.__header = Label(self, text="Main page")
        self.__header.grid(row=0, column=0, columnspan=2)

        # notebook

        self.__navigation_notebook = Notebook(self)
        self.__navigation_notebook.grid(row=1, column=0, columnspan=2)

        self.bank_action_frame = BankActionFrame(self.user, self.database, self.__navigation_notebook)
        self.log_frame = LogFrame(self.user, self.__navigation_notebook)

        self.__navigation_notebook.add(self.bank_action_frame, text="Account action")
        self.__navigation_notebook.add(self.log_frame, text="Bank log")
        self.__admin_frame = AdminFrame(self.database, self.__navigation_notebook)

        if self.user.is_admin():
            self.__navigation_notebook.add(self.__admin_frame, text="Admin")

        self.__navigation_notebook.bind('<<NotebookTabChanged>>', self.refresh_frames)

        # buttons

        self.__log_off_button = Button(self, text="Log off", command=lambda: root.open_login_frame())
        self.__quit_button = Button(self, text="Quit", command=lambda: root.quit())

        self.__log_off_button.grid(row=2, column=0)
        self.__quit_button.grid(row=2, column=1)

    def refresh_frames(self, *args):
        """

        :return:
        """

        self.log_frame.update_log()
        self.__admin_frame.update_user_balances()


class BankActionFrame(Frame):
    """

    """

    def __init__(self, current_user, database, root=None):
        """

        :param current_user:
        :param root:
        """

        super().__init__(root)
        self.user = current_user
        self.database = database

        # StringVars

        self.__balance = StringVar(self)
        self.__receiver = StringVar(self)
        self.__deposit = StringVar(self)
        self.__withdraw = StringVar(self)
        self.__transfer = StringVar(self)

        self.__balance.set(f"{self.user.balance:.2f} €")
        self.__deposit.set("0.00")
        self.__withdraw.set("0.00")
        self.__transfer.set("0.00")

        # labels

        self.__header = Label(self, text="Account action")
        self.__current_balance_label = Label(self, textvariable=self.__balance)
        self.__deposit_label = Label(self, text="Deposit")
        self.__withdraw_label = Label(self, text="Withdraw")
        self.__transfer_label = Label(self, text="Transfer")
        self.__receiver_label = Label(self, text="Receiver")
        self.action_label = Label(self)

        # buttons

        self.__deposit_button = Button(self, text="Deposit", command=self.deposit)
        self.__withdraw_button = Button(self, text="Withdraw", command=self.withdraw)
        self.__transfer_button = Button(self, text="Transfer", command=self.transfer)

        # entry

        self.__receiver_entry = Entry(self, textvariable=self.__receiver)

        # spinboxes

        self.__deposit_spinbox = Spinbox(self, from_=0.00, to=1000.00,
                                         increment=0.01, textvariable=self.__deposit)
        self.__withdraw_spinbox = Spinbox(self, from_=0.00, to=1000.00,
                                          increment=0.01, textvariable=self.__withdraw)
        self.__transfer_spinbox = Spinbox(self, from_=0.00, to=1000.00,
                                          increment=0.01, textvariable=self.__transfer)

        # placing the widgets

        self.__header.grid(row=0, column=0, columnspan=2)

        self.__current_balance_label.grid(row=1, column=0, columnspan=2)

        self.__deposit_label.grid(row=2, column=0, columnspan=2)
        self.__deposit_spinbox.grid(row=3, column=0)
        self.__deposit_button.grid(row=3, column=1)

        self.__withdraw_label.grid(row=4, column=0, columnspan=2)
        self.__withdraw_spinbox.grid(row=5, column=0)
        self.__withdraw_button.grid(row=5, column=1)

        self.__transfer_label.grid(row=6, column=0, columnspan=2)
        self.__receiver_label.grid(row=7, column=0)
        self.__receiver_entry.grid(row=7, column=1)
        self.__transfer_spinbox.grid(row=8, column=0)
        self.__transfer_button.grid(row=8, column=1)

        self.action_label.grid(row=9, column=0, columnspan=2)

    def deposit(self):
        """

        :return:
        """

        try:
            sum = float(self.__deposit_spinbox.get())

        except ValueError:
            self.action_label["text"] = "Error: You must input a number"
            self.reset_fields()
            return

        if self.user.deposit(sum):
            self.action_label["text"] = f"Deposited {sum:.2f} €"
            self.__balance.set(f"{self.user.balance:.2f} €")

        else:
            self.action_label["text"] = "Error: You can't deposit a negative amount of money"

        self.reset_fields()

    def withdraw(self):
        """

        :return:
        """

        try:
            sum = float(self.__deposit_spinbox.get())

        except ValueError:
            self.action_label["text"] = "Error: You must input a number"
            self.reset_fields()
            return

        withdrawal = self.user.withdraw(sum)

        if withdrawal:
            self.action_label["text"] = f"Withdrew {withdrawal:.2f} €"
            self.__balance.set(f"{self.user.balance:.2f} €")

        else:
            self.action_label["text"] = "Error: You cannot withdraw a negative amount of money"

        self.reset_fields()

    def transfer(self):
        """

        :return:
        """

        try:
            sum = float(self.__transfer_spinbox.get())

        except ValueError:
            self.action_label["text"] = "Error: You must input a number"
            self.reset_fields()
            return

        if self.__receiver.get() not in self.database:
            self.action_label["text"] = "Error: Other user cannot be found"
            self.reset_fields()
            return

        target = self.database.get_user(self.__receiver.get())

        actual_sum = self.user.transfer(target, sum)
        if actual_sum:
            self.action_label["text"] = f"Transferred {actual_sum:.2f} € to {target}"
            self.__balance.set(f"{self.user.balance:.2f} €")

        else:
            self.action_label["text"] = "Error: You cannot transfer a negative amount of money"

        self.reset_fields()

    def reset_fields(self):
        """

        :return:
        """
        self.__deposit.set("0.00")
        self.__withdraw.set("0.00")
        self.__transfer.set("0.00")
        self.__receiver.set("")


class LogFrame(Frame):
    """

    """

    def __init__(self, current_user, root=None):
        """

        :param current_user:
        :param root:
        """

        super().__init__(root)
        self.current_user = current_user

        # Labels

        self.__header = Label(self, text="Account history")

        self.current_entries = []

        for entry in self.current_user.log:
            log_label = Label(self, text=entry)
            log_label.pack()
            self.current_entries.append(entry)

        self.__header.pack()

    def update_log(self):
        """

        :return:
        """

        log = self.current_user.log

        # delete all the log entries that already exist

        try:
            while log[0] == self.current_entries[0]:
                del log[0]

        except IndexError:
            pass

        for entry in log:
            log_label = Label(self, text=entry)
            log_label.pack()
            self.current_entries.append(entry)


class AdminFrame(Frame):
    """

    """

    def __init__(self, database, root=None):
        """

        :param database:
        :param root:
        """

        super().__init__(root)
        self.database = database

        self.users = self.database.get_all_users()
        self.balance_stringvars = {}

        row = 0
        for user in self.users:
            balance = StringVar()
            balance.set(f"{user.balance:.2f} €")

            # widgets for each user

            user_frame = Frame(self)
            username_label = Label(user_frame, text=user)
            balance_label = Label(user_frame, textvariable=balance)

            username_label.grid(row=row, column=0)
            balance_label.grid(row=row, column=1)
            user_frame.grid(row=row, column=0)

            self.balance_stringvars[user] = balance

            row += 1

    def update_user_balances(self):
        """

        :return:
        """

        for user in self.users:
            self.balance_stringvars[user].set(f"{user.balance:.2f} €")


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
        self.balance = 0.0
        self.log = []

    def __str__(self):
        """
        returns the Accounts username
        :return: str, the username
        """

        return self.__username

    def deposit(self, money):
        """
        This method adds money to the account's balance
        :param money: float, the amount of money to be added
        :return: bool, has the action been successful
        """

        if money < 0:
            return False

        self.balance += money
        self.log.append(f"+{money:.2f} €:   Deposit")

        return True

    def withdraw(self, money):
        """
        This method removes money from the account's balance
        :param money: float, the amount of money to be removed
        :return: False if the action fails
        """

        if money < 0:
            return False

        elif self.balance - money < 0:
            money = self.balance
            self.balance = 0

        else:
            self.balance -= money

        self.log.append(f"-{money:.2f} €:   Withdrawal")
        return money

    def transfer(self, other_account, money):
        """
        This method transfers money to another account and adds it to the log
        :param other_account: Account, the account the money is getting transferred to
        :param money: float, the amount of money to be
        :return: str, the error type if something goes wrong
        """

        if money < 0:
            return False

        elif self.balance - money < 0:
            money = self.balance

            self.balance = 0
            other_account.balance += money

        else:
            self.balance -= money
            other_account.balance += money

        self.log.append(f"-{money:.2f} €:   Transfer to {other_account}")
        other_account.log.append(f"+{money:.2f} €:   Transfer from {self}")

        return money

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

        self.__database = {"admin": {"user": Account("admin", True), "password": "admin"}}
        self.add_user("test1", "test")
        self.add_user("test2", "test")
        self.add_user("test3", "test")
        self.add_user("test4", "test")

    def __contains__(self, item):
        """

        :param item:
        :return:
        """

        return item in self.__database

    def add_user(self, username, password):
        """
        adds the user to the database
        :param username: str, the username
        :param password: str, the password
        """

        user = Account(username)
        self.__database[username] = {"user": user, "password": password}

    def check_credentials(self, username, password):
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

    def get_all_users(self):
        """

        :return:
        """

        key_list = self.__database.keys()
        users = []

        for key in key_list:
            users.append(self.__database[key]["user"])

        return users


def main():
    app = App()
    app.start()


if __name__ == "__main__":
    main()

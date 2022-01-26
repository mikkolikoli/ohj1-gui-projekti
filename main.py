"""
This is a banking program with different account functionality.
For the management of the users I have made a class named "UserDatabase". The main data structure inside is a dict
After logging in, the user will have either 2 or 3 possible pages to check out. On the first page, you can deposit or
withdraw money from their account or they can transfer money to another account.
The second page shows their bank log. Whenever they do anything on the first page, it will be added to the second page.
The user also gets feedback on the bank action page whenever they do something, whether that may be getting an error
or showing the user that their action was successful.
If the user is an admin, they'll see a third page named 'admin' which shows every user's balance.

The default admin credentials are
username: admin
password: admin

these can only be changed in the source code, as the default state of a new user's admin attribute is False.

I could probably optimize the code in many ways but I have had enough weird bugs already and not enough time to fix
every potential bug that would come about from optimizing the code. Also some methods or attributes may be unnecessary.


Name:        Mikko Rajakorpi
Email:       mikko.rajakorpi@tuni.fi
Student ID:  150464570
"""


import tkinter.messagebox
from tkinter import *
from tkinter.ttk import *


class App(Tk):
    """
    The window class. This class has all the login and register functionality. Inherits from Tk.
    """

    def __init__(self):
        """
        Constructor.
        """

        super().__init__()
        self.database = UserDatabase()
        self.login_frame = LoginFrame(self)
        self.register_frame = RegisterFrame(self)
        self.main_frame = None

        self.wm_title("Banking program")

        self.currently_open_frame = self.login_frame

        self.login_frame.pack()

    def start(self):
        """
        starts the program
        """

        self.mainloop()

    def close(self):
        """
        closes the program
        """

        self.destroy()

    def login(self, username, password):
        """
        A method for the login process
        :param username: str, the username
        :param password: str, the password
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
    A class managing the login frame. This class only creates the frame. Functionality is in the App class.
    Inherits from Frame.
    """

    def __init__(self, root):
        """
        Constructor.
        :param root: the frame's root
        """

        super().__init__(root)

        # labels

        self.header = Label(self, text="Login", font=("Arial", 16))
        self.username_label = Label(self, text="Username")
        self.password_label = Label(self, text="Password")
        self.error_label = Label(self)
        self.register_label = Label(self, text="Don't have an account yet?")

        # entries and their StringVars

        self.username = StringVar(self)
        self.password = StringVar(self)
        self.username_entry = Entry(self, textvariable=self.username)
        self.password_entry = Entry(self, textvariable=self.password, show="*")

        # buttons

        self.login_button = Button(self, text="Login", command=lambda: root.login(self.username.get(),
                                                                                  self.password.get()))
        self.register_button = Button(self, text="Create an account", command=lambda: root.open_register_frame())
        self.quit_button = Button(self, text="Quit", command=lambda: root.close())

        # placing the widgets

        self.header.grid(row=0, column=0, columnspan=3, pady=10)

        self.username_label.grid(row=1, column=0)
        self.username_entry.grid(row=1, column=1)
        self.password_label.grid(row=2, column=0)
        self.password_entry.grid(row=2, column=1)

        self.error_label.grid(row=3, column=1)

        self.login_button.grid(row=4, column=1)
        self.register_label.grid(row=5, column=1)
        self.register_button.grid(row=6, column=1)

        self.quit_button.grid(row=7, column=2)

    def show_error_message(self, text):
        """
        shows an error message
        :param text: str, the error message
        """

        self.error_label["text"] = text
        self.reset_fields()

    def reset_fields(self):
        """
        clears the entry fields
        """

        self.username.set("")
        self.password.set("")


class RegisterFrame(Frame):
    """
    The class managing the register frame. The main functions of the frame are in the App class.
    This class only manages the ui. Inherits from Frame
    """

    def __init__(self, root):
        """
        Constructor
        :param root: the frame's root
        """

        super().__init__(root)

        # creating a StringVar for updates to the password_security progressbar on each update on the password entry

        self.username = StringVar(self)
        self.password = StringVar(self)
        self.repeat_password = StringVar(self)
        self.password.trace("w", self.strength)

        # labels

        self.header = Label(self, text="Register", font=("Arial", 16))
        self.username_label = Label(self, text="Username")
        self.password_label = Label(self, text="Password")
        self.repeat_password_label = Label(self, text="Repeat password")
        self.password_security_label = Label(self, text="Password strength: Weak")
        self.login_label = Label(self, text="Already got an account? Log in instead")
        self.error_label = Label(self)

        # entry fields

        self.username_entry = Entry(self, textvariable=self.username)
        self.password_entry = Entry(self, textvariable=self.password, show="*")
        self.repeat_password_entry = Entry(self, textvariable=self.repeat_password, show="*")

        # buttons

        self.register_button = Button(self, text="Register",
                                      command=lambda: root.register(self.username.get(), self.password.get(),
                                                                    self.repeat_password.get()))
        self.login_button = Button(self, text="Login", command=lambda: root.open_login_frame())
        self.quit_button = Button(self, text="Quit", command=lambda: root.close())

        # progressbar

        self.password_security = Progressbar(self, orient=HORIZONTAL, length=100, mode="determinate")

        # placing the widgets

        self.header.grid(row=0, column=1, pady=10)

        self.username_label.grid(row=1, column=0, sticky=E)
        self.username_entry.grid(row=1, column=1)
        self.password_label.grid(row=2, column=0, sticky=E)
        self.password_entry.grid(row=2, column=1)
        self.repeat_password_label.grid(row=3, column=0, sticky=E)
        self.repeat_password_entry.grid(row=3, column=1)

        self.error_label.grid(row=4, column=1)

        self.password_security_label.grid(row=5, column=1)
        self.password_security.grid(row=6, column=1)
        self.register_button.grid(row=7, column=1)

        self.login_label.grid(row=8, column=1)
        self.login_button.grid(row=9, column=1)

        self.quit_button.grid(row=10, column=2)

    def show_error_message(self, text):
        """
        shows an error message
        :param text: str, the error message
        """

        self.error_label["text"] = text
        self.reset_fields()

    def reset_fields(self):
        """
        clears the entry fields
        """

        self.username.set("")
        self.password.set("")
        self.repeat_password.set("")

    def strength(self, *args):
        """
        A method to show the strength of the password entered by the user in the progressbar and the label for the
        password strength
        :param args: fix for an error I had with the self.password.trace() command
        """

        password = self.password.get()

        if 0 <= len(password) <= 8:
            self.password_security["value"] = 0
            self.password_security_label["text"] = "Password strength: Weak"

        elif 8 < len(password) <= 12:
            self.password_security["value"] = 50
            self.password_security_label["text"] = "Password strength: Medium"

            if any(char.isdigit() for char in password):
                self.password_security["value"] = 100
                self.password_security_label["text"] = "Password strength: Strong"

        else:
            self.password_security["value"] = 100

            self.password_security_label["text"] = "Password strength: Strong"


class MainUiFrame(Frame):
    """
    A class managing the main ui's frame. The main page manages all its subframes in a notebook. Inherits from Frame
    """

    def __init__(self, current_user, database, root):
        """
        Constructor.
        :param current_user: Account, the user that's currently logged in, used to check if the user is an admin.
        :param database: UserDatabase, the main user database
        :param root: the frame's root
        """

        super().__init__(root)

        self.user = current_user
        self.database = database

        # balance StringVar

        self.balance = StringVar(root)
        self.balance.set(self.user.balance)

        # notebook

        self.navigation_notebook = Notebook(self)
        self.navigation_notebook.grid(row=1, column=0, columnspan=2)

        self.bank_action_frame = BankActionFrame(self.user, self.database, self.navigation_notebook)
        self.log_frame = LogFrame(self.user, self.navigation_notebook)

        self.navigation_notebook.add(self.bank_action_frame, text="Account action")
        self.navigation_notebook.add(self.log_frame, text="Bank log")
        self.admin_frame = AdminFrame(self.database, self.navigation_notebook)

        if self.user.is_admin():
            self.navigation_notebook.add(self.admin_frame, text="Admin")

        self.navigation_notebook.bind('<<NotebookTabChanged>>', self.refresh_frames)

        # label

        self.header = Label(self, text=self.navigation_notebook.tab(self.navigation_notebook.select(), "text"),
                            font=("Arial", 16))
        self.header.grid(row=0, column=0, columnspan=2, pady=10)

        # buttons

        self.log_off_button = Button(self, text="Log off", command=lambda: root.open_login_frame())
        self.quit_button = Button(self, text="Quit", command=lambda: root.quit())

        self.log_off_button.grid(row=2, column=0)
        self.quit_button.grid(row=2, column=1)

    def refresh_frames(self, *args):
        """
        refreshes all frames, necessary to keep the bank log and admin frames updated in realtime
        :param args: a fix for an error I got when calling this method
        """

        self.log_frame.update_log()
        self.admin_frame.update_user_data()

        self.header["text"] = self.navigation_notebook.tab(self.navigation_notebook.select(), "text")


class BankActionFrame(Frame):
    """
    A method managing the bank action frame with the main functions of the banking program
    """

    def __init__(self, current_user, database, root):
        """
        Constructor
        :param current_user: Account, the user currently logged in
        :param root: the frame's root
        """

        super().__init__(root)
        self.user = current_user
        self.database = database

        # StringVars

        self.balance = StringVar(self)
        self.target = StringVar(self)
        self.deposit_sum = StringVar(self)
        self.withdraw_sum = StringVar(self)
        self.transfer_sum = StringVar(self)

        self.balance.set(f"{self.user.balance:.2f} €")
        self.deposit_sum.set("0.00")
        self.withdraw_sum.set("0.00")
        self.transfer_sum.set("0.00")

        # labels

        self.current_balance_label = Label(self, textvariable=self.balance, font=("Arial", 14))
        self.deposit_label = Label(self, text="Deposit", font=("Arial", 14))
        self.withdraw_label = Label(self, text="Withdraw", font=("Arial", 14))
        self.transfer_label = Label(self, text="Transfer", font=("Arial", 14))
        self.target_label = Label(self, text="Receiver")
        self.action_label = Label(self)

        # buttons

        self.deposit_button = Button(self, text="Deposit", command=self.deposit)
        self.withdraw_button = Button(self, text="Withdraw", command=self.withdraw)
        self.transfer_button = Button(self, text="Transfer", command=self.transfer)

        # entry

        self.target_entry = Entry(self, textvariable=self.target, width=15)

        # spinboxes

        self.deposit_spinbox = Spinbox(self, from_=0.00, to=1000.00,
                                       increment=0.01, textvariable=self.deposit_sum, width=7)
        self.withdraw_spinbox = Spinbox(self, from_=0.00, to=1000.00,
                                        increment=0.01, textvariable=self.withdraw_sum, width=7)
        self.transfer_spinbox = Spinbox(self, from_=0.00, to=1000.00,
                                        increment=0.01, textvariable=self.transfer_sum, width=7)

        # placing the widgets

        self.current_balance_label.grid(row=1, column=0, columnspan=2, pady=5)

        self.deposit_label.grid(row=2, column=0, columnspan=2, pady=5)
        self.deposit_spinbox.grid(row=3, column=0)
        self.deposit_button.grid(row=3, column=1)

        self.withdraw_label.grid(row=4, column=0, columnspan=2, pady=5)
        self.withdraw_spinbox.grid(row=5, column=0)
        self.withdraw_button.grid(row=5, column=1)

        self.transfer_label.grid(row=6, column=0, columnspan=2, pady=5)
        self.target_label.grid(row=7, column=1, sticky=W)
        self.target_entry.grid(row=8, column=1)
        self.transfer_spinbox.grid(row=8, column=0, padx=20)
        self.transfer_button.grid(row=9, column=0, columnspan=2)

        self.action_label.grid(row=10, column=0, columnspan=2)

    def deposit(self):
        """
        A method to deposit money into the current users account
        """

        try:
            sum = float(self.deposit_spinbox.get())

        except ValueError:
            self.action_label["text"] = "Error: You must input a number"
            self.reset_fields()
            return

        if self.user.deposit(sum):
            self.action_label["text"] = f"Deposited {sum:.2f} €"
            self.balance.set(f"{self.user.balance:.2f} €")

        else:
            self.action_label["text"] = "Error: You must input a positive number"

        self.reset_fields()

    def withdraw(self):
        """
        A method to withdraw money from the current user's account
        """

        try:
            sum = float(self.withdraw_spinbox.get())

        except ValueError:
            self.action_label["text"] = "Error: You must input a number"
            self.reset_fields()
            return

        actual_sum = self.user.withdraw(sum)

        if actual_sum:
            self.action_label["text"] = f"Withdrew {actual_sum:.2f} €"
            self.balance.set(f"{self.user.balance:.2f} €")

        else:
            self.action_label["text"] = "Error: You must input a positive number"

        self.reset_fields()

    def transfer(self):
        """
        A method to transfer money from the current user's account to another account
        """

        try:
            sum = float(self.transfer_spinbox.get())

        except ValueError:
            self.action_label["text"] = "Error: You must input a number"
            self.reset_fields()
            return

        if self.target.get() not in self.database:
            self.action_label["text"] = "Error: Other user cannot be found"
            self.reset_fields()
            return

        target = self.database.get_user(self.target.get())

        actual_sum = self.user.transfer(target, sum)

        if actual_sum:
            self.action_label["text"] = f"Transferred {actual_sum:.2f} € to {target}"
            self.balance.set(f"{self.user.balance:.2f} €")

        else:
            self.action_label["text"] = "Error: You must input a positive number"

        self.reset_fields()

    def reset_fields(self):
        """
        A method to reset all the fields
        """
        self.deposit_sum.set("0.00")
        self.withdraw_sum.set("0.00")
        self.transfer_sum.set("0.00")
        self.target.set("")


class LogFrame(Frame):
    """
    A class managing the log frame. Inherits from Frame
    """

    def __init__(self, current_user, root):
        """
        Constructor.
        :param current_user: Account, the account that is currently logged in
        :param root: the frame's root
        """

        super().__init__(root)
        self.current_user = current_user
        self.current_entries = []

        # balance label

        self.balance = StringVar(self)
        self.balance.set(f"{self.current_user.balance} €")

        self.balance_label = Label(self, textvariable=self.balance, font=("Arial", 14))
        self.balance_label.pack(pady=10)

        # creates a label each for every log entry

        for entry in self.current_user.log:
            log_label = Label(self, text=entry)
            log_label.pack()
            self.current_entries.append(entry)

    def update_log(self):
        """
        A method to update the log frame. Necessary to have it show the log in realtime after making changes
        """

        log = self.current_user.log

        # updates the balance

        self.balance.set(f"{self.current_user.balance} €")

        # adds all the new log entries to the frame

        if log:
            for i in range(len(self.current_entries), len(log)):
                log_label = Label(self, text=log[i])
                log_label.pack()
                self.current_entries.append(log[i])


class AdminFrame(Frame):
    """
    A class managing the admin frame. Inherits from Frame
    """

    def __init__(self, database, root):
        """
        Constructor
        :param database: UserDatabase, the main database
        :param root: the frame's root
        """

        super().__init__(root)
        self.database = database

        self.users = self.database.get_all_users()

        # dicts for the different widgets

        self.balance_stringvars = {}
        self.user_frames = {}

        # Label for feedback for user action

        self.action_label = Label(self)

        # labels for each user

        row = 0
        for user in self.users:
            balance = StringVar()
            balance.set(f"{user.balance:.2f} €")
            self.balance_stringvars[user] = balance

            # widgets for each user

            user_frame = Frame(self)
            username_label = Label(user_frame, text=user)
            balance_label = Label(user_frame, textvariable=balance)

            self.user_frames[user] = user_frame

            username_label.grid(row=0, column=0, padx=50, sticky=W)
            balance_label.grid(row=0, column=1, padx=50, sticky=E)
            user_frame.grid(row=row, column=0, pady=5)

            row += 1

        self.action_label.grid(row=row, column=0, columnspan=3)

    def update_user_data(self):
        """
        Updates the balances of each user. Necessary for realtime changes in the ui
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

        self.username = username
        self.admin = admin
        self.balance = 0.0
        self.log = []

    def __str__(self):
        """
        returns the Accounts username
        :return: str, the username
        """

        return self.username

    def deposit(self, sum):
        """
        This method adds money to the account's balance
        :param sum: float, the amount of money to be added
        :return: bool, has the action been successful
        """

        if sum <= 0:
            return False

        self.balance += sum

        # adds the transaction to the user's log

        self.log.append(f"+{sum:.2f} €:   Deposit")
        return True

    def withdraw(self, sum):
        """
        This method removes money from the account's balance
        :param sum: float, the amount of money to be removed
        :return: False if the action fails, the actual money that got withdrawn if it succeeds
        """

        if sum <= 0:
            return False

        elif self.balance - sum < 0:
            sum = self.balance
            self.balance = 0

        else:
            self.balance -= sum

        # adds the transaction to the user's log

        self.log.append(f"-{sum:.2f} €:   Withdrawal")
        return sum

    def transfer(self, target, sum):
        """
        This method transfers money to another account and adds it to the log
        :param target: Account, the account the money is getting transferred to
        :param sum: float, the amount of money to be
        :return: False if the action fails, the actual money that got withdrawn if it succeeds
        """

        if sum <= 0:
            return False

        elif self.balance - sum < 0:
            sum = self.balance

            self.balance = 0
            target.balance += sum

        else:
            self.balance -= sum
            target.balance += sum

        # adds the transaction to both the user's logs

        self.log.append(f"-{sum:.2f} €:   Transfer to {target}")
        target.log.append(f"+{sum:.2f} €:   Transfer from {self}")
        return sum

    def is_admin(self):
        """
        returns whether the user is an admin
        """

        return self.admin


class UserDatabase:
    """
    saves all the user data
    """

    def __init__(self):
        """
        Constructor. Database is a dict
        """

        self.database = {"admin": {"user": Account("admin", True), "password": "admin"}}

    def __contains__(self, item):
        """
        Used for checking if a user already exists
        :param item: str, the username of the person that will be checked
        :return: bool
        """

        return item in self.database

    def add_user(self, username, password):
        """
        adds the user to the database
        :param username: str, the username
        :param password: str, the password
        """

        user = Account(username)
        self.database[username] = {"user": user, "password": password}

    def check_credentials(self, username, password):
        """
        checks if the username and password are correct
        :param username: str, the username
        :param password: str, the password
        :return: bool, are the username and password correct
        """

        if username in self.database and self.database[username]["password"] == password:
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

        if username in self.database:
            return self.database[username]["user"]

        else:
            return False

    def get_all_users(self):
        """
        creates a list of all the users and returns it
        :return: list, list of objects of class Account
        """

        key_list = self.database.keys()
        users = []

        for key in key_list:
            users.append(self.database[key]["user"])

        return users


def main():
    app = App()
    app.start()


if __name__ == "__main__":
    main()

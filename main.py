""" UAT Dashboard

This script creates a graphical user interface for running the different UAT test scripts. 
This interface is made with customtkinter which is a UI library based on tkinter 
This script also utilizes threading to run scripts without freezing the GUI 
This file contains the UI layouts and the processes needed to run the scripts from the GUI 
When adding a new test: import the test, modify: TestSelection to add a checkbox, run_next_task to run the test, and start_test to append the test
"""
import customtkinter
from create_client_test import create_client_test
from search_client_test import search_client_test
from edit_existing_test import edit_existing
from family_modification_test import family_test
from merge_accounts_test import merge_test
from logs_test import log_test
from customer_adjustment_test import adjustment_test
from document_test import document_test
from communication_test import communication_test
from search_account_test import search_account_test
from create_account_test import create_account_test
from send_email_test import send_email_test
from threading import Thread
from queue import Queue

# Enter Test Login UI (Login fields)
class LoginDetails(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.email = customtkinter.CTkEntry(self, placeholder_text="Enter Email")
        self.email.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="w")
        self.password = customtkinter.CTkEntry(self, placeholder_text="Enter Password", show="*")
        self.password.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.show_password = customtkinter.CTkCheckBox(self, text="Show Password", command=self.toggle_show_password)
        self.show_password.grid(row=3, column=0, padx=10, pady=10)
    
    # Function to toggle showing the password
    def toggle_show_password(self):
        if self.password.cget("show") == "*":
                self.password.configure(show = "")
        else:
                self.password.configure(show = "*")

# Test Selection UI (Checkbox selections)
class TestSelection(customtkinter.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master)
        self.checkbox1 = customtkinter.CTkCheckBox(self, text="Create a Client")
        self.checkbox1.grid(row=1, column=0, padx=10, pady=10, sticky="nsw")
        self.checkbox2 = customtkinter.CTkCheckBox(self, text="Search for Client")
        self.checkbox2.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.checkbox3 = customtkinter.CTkCheckBox(self, text="Edit Existing Client")
        self.checkbox3.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.checkbox4 = customtkinter.CTkCheckBox(self, text="Family Members")
        self.checkbox4.grid(row=4, column=0, padx=10, pady=10, sticky="w")
        self.checkbox5 = customtkinter.CTkCheckBox(self, text="Merge Accounts")
        self.checkbox5.grid(row=5, column=0, padx=10, pady=10, sticky="w")
        self.checkbox6 = customtkinter.CTkCheckBox(self, text="Create Logs")
        self.checkbox6.grid(row=6, column=0, padx=10, pady=10, sticky="w")
        self.checkbox7 = customtkinter.CTkCheckBox(self, text="Customer Adjustment")
        self.checkbox7.grid(row=7, column=0, padx=10, pady=10, sticky="w")
        self.checkbox8 = customtkinter.CTkCheckBox(self, text="Documents")
        self.checkbox8.grid(row=8, column=0, padx=10, pady=10, sticky="w")
        self.checkbox9 = customtkinter.CTkCheckBox(self, text="Communications")
        self.checkbox9.grid(row=9, column=0, padx=10, pady=10, sticky="w")
        self.checkbox10 = customtkinter.CTkCheckBox(self, text="Search for Account")
        self.checkbox10.grid(row=10, column=0, padx=10, pady=10, sticky="w")
        self.checkbox11 = customtkinter.CTkCheckBox(self, text="Create an Account")
        self.checkbox11.grid(row=11, column=0, padx=10, pady=10, sticky="w")
        self.checkbox12 = customtkinter.CTkCheckBox(self, text="Send an Email")
        self.checkbox12.grid(row=12, column=0, padx=10, pady=10, sticky="w")

# Test Results UI (Textbox on the right)
class Logs(customtkinter.CTkFrame):
    def __init__(self,master):
        super().__init__(master)
        self.box = customtkinter.CTkTextbox(master=self,   corner_radius=15)
        self.box.insert("0.0", "Test Results:")
        self.box.configure(state="disabled")
        self.box.grid(row=0, column=0)

def check_queue(self,q):
    """
    Checks that the queue shared with the threads running the tests are populated

    Parameters:
    self (App): The instance of the GUI to be passed to the modify_log() function
    q (Queue): The queue shared among the threads

    Returns:
    None
    """
    while True:
        if not q.empty():
            modify_log(self, q.get())
            break
        else:
            pass

def modify_log(self, messages):
    """
    Modifies the textbox in the GUI to display text

    Parameters:
    self (App): The instance of the GUI
    messages (str[]): An array of strings of the messages that should be displayed in the log 

    Returns:
    None

    """
    self.text.box.configure(state='normal')
    #self.text.box.delete("0.0",'end')
    for i in messages:
        self.text.box.insert("end",i+'\n')
    self.text.box.configure(state = 'disabled')

def start_thread(self, test, email, password, headless):
    """Creates and starts the thread for a test. 
    Creates another thread to determine if the test is done and to update the UI
    Also creates a queue so that the threads can communicate.

    Parameters:
    self: is the instance of the app
    test: Callable(function) is the selected test
    email (str): is the email used to login
    password (str): is the password used to login
    headless (bool): is the user decision to run headless or not

    Returns:
    None

    """
    q = Queue()
    thread = Thread(target=test, args=(q, email, password, headless))
    thread2 = Thread(target=check_queue, args=(self,q))
    thread.start()
    thread2.start()
    thread.join()
    
def run_next_task(self, tasks, index, email, password, headless):
    """Runs the determines tests selected to run and creates a new thread for each of the tests. 

    Parameters:
    self: is the instance of the app 
    tasks (list of int): is the array of the tasks selected, each task is given a number in the array
    index (int): is the index of the current task
    email (str): is the email used to login
    password (str): is the password used to login
    headless (bool): is the user choice of whether they want the test to run headless or not

    Returns:
    None
    """
    if index < len(tasks):
        task = tasks[index]
        if task == 1:
            modify_log(self, ['Starting Create Client Test'])
            start_thread(self, create_client_test, email,password,headless)
        elif task == 2:
            modify_log(self, ['Starting Search Client Test'])
            start_thread(self, search_client_test,email,password,headless)
        elif task == 3:
            modify_log(self, ['Starting Edit Client Test'])
            start_thread(self, edit_existing,email,password,headless)
        elif task == 4:
            modify_log(self, ['Starting Family Test'])
            start_thread(self, family_test,email,password,headless)
        elif task == 5:
            modify_log(self, ['Starting Merge Test'])
            start_thread(self, merge_test, email, password, headless)
        elif task == 6:
            modify_log(self, ['Starting Create Log Test'])
            start_thread(self, log_test, email, password, headless)
        elif task == 7:
            modify_log(self, ['Starting Customer Adjustment Test'])
            start_thread(self, adjustment_test, email, password, headless)
        elif task == 8:
            modify_log(self, ['Starting Document Test'])
            start_thread(self, document_test, email, password, headless)
        elif task == 9:
            modify_log(self, ['Starting Communication Test'])
            start_thread(self, communication_test, email, password, headless)
        elif task == 10:
            modify_log(self, ['Starting Search Account Test'])
            start_thread(self, search_account_test, email, password, headless)
        elif task == 11:
            modify_log(self, ['Starting Create Account Test'])
            start_thread(self, create_account_test, email, password, headless)
        elif task == 12:
             modify_log(self, ['Starting Sending Email Test'])
             start_thread(self, send_email_test, email, password, headless)
        run_next_task(self, tasks, index+1, email, password, headless)

# Class for the desktop GUI of the application 
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("UAT Testing Dashboard")
        self.geometry("720x480")
        
        # Test Login
        self.login_label = customtkinter.CTkLabel(self, text="Enter Test Login ", font=('Helvetica', 16, 'bold'), padx=10)
        self.login_label.grid(row=0, column=0, sticky="nw")
        self.login = LoginDetails(self)
        self.login.grid(row=1, column=0, padx=10, pady=10, sticky="nsw")
        
        # Test Selection
        self.test_label = customtkinter.CTkLabel(self, text="Select Tests", font=('Helvetica', 16, 'bold'), padx=10)
        self.test_label.grid(row=0, column=1, sticky="nw")
        self.test = TestSelection(self)
        self.test.grid(row=1, column=1, padx=10, pady=10, sticky="nsw")

        # Test Results/Log
        self.text_label = customtkinter.CTkLabel(self, text="Test Results", font=('Helvetica', 16, 'bold'), padx=10)
        self.text_label.grid(row=0, column=2, sticky="nw")
        self.text = Logs(self)
        self.text.grid(row=1, column=2, padx=10, pady=10, sticky="nsw")

        # Headless Toggle
        self.switch = customtkinter.CTkSwitch(self, text="Headless")
        self.switch.grid(row=3, column=0, padx=10, pady=10)
        
        # Start Tests Button 
        self.button = customtkinter.CTkButton(self, text="Start Tests", command=self.start_tests)
        self.button.grid(row=3, column=1, padx=10, pady=10, sticky="sew")

    # Start function for running tests
    def start_tests(self):
        # Get data from fields 
        email = self.login.email.get()
        password = self.login.password.get()
        headless = self.switch.get()

        # Get the selected tests and append numbers corresponding to the checkbox to the test selection array 
        test_selection = []
        if self.test.checkbox1.get() == 1:
            test_selection.append(1)
        if self.test.checkbox2.get() == 1:
            test_selection.append(2)
        if self.test.checkbox3.get() == 1:
            test_selection.append(3)
        if self.test.checkbox4.get() == 1:
            test_selection.append(4)
        if self.test.checkbox5.get() == 1:
            test_selection.append(5)
        if self.test.checkbox6.get() == 1:
            test_selection.append(6)
        if self.test.checkbox7.get() == 1:
            test_selection.append(7)
        if self.test.checkbox8.get() == 1:
            test_selection.append(8)
        if self.test.checkbox9.get() == 1:
            test_selection.append(9)
        if self.test.checkbox10.get() == 1:
            test_selection.append(10)
        if self.test.checkbox11.get() == 1:
            test_selection.append(11)
        if self.test.checkbox12.get() == 1:
            test_selection.append(12)

        # Check that email, password, and test selection fields are populated before running 
        if ((not len(email) == 0 and not len(password) == 0) and len(test_selection) > 0):
            self.text.box.configure(state='normal')
            self.text.box.delete("0.0",'end')
            modify_log(self, ['Started Tests!'])
            thread = Thread(target = run_next_task, args=(self, test_selection, 0, email, password, headless))
            thread.start()
        # Inform user that they have to enter login details if email and/or password field is blank
        else:
            modify_log(self, ['Please enter login details to start'])

# Create an instance of the App and run it in a mainloop to start the GUI
app = App()
app.mainloop()
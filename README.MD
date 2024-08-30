## How to use this program:
- Make sure you have python and selenium installed on your computer
    - To install python, go to https://www.python.org/downloads/ and click download on the latest version
    - To install selenium, you will: 
        - Click the windows button 
        - Type "CMD" into the search bar 
        - Click on command prompt 
        - Type `pip install selenium` and press enter
- Install Visual Studio Code from https://code.visualstudio.com/ and download the latest version
- When you open Visual Studio Code, you will have the option to open a folder. Select the UAT Scripts folder and click open. Click trust the authors if it prompts you.
- Open After installing everything, navigate to the `main.py` in this folder
    - Option 1: Near the top right, there should be a triangle that says 'Run Python File', click this button
	- Option 2: In the top menu of the screen, navigate to "Terminal" and click "New Terminal"
	    - After clicking, there will be a box near the bottom of your screen that prompts you to enter something. Enter `python main.py`
## How the program is organized:
- main.py holds the code needed to create the GUI dashboard and run the test that are created
- all tests have `<name of test>_test.py` as their file name, more about the tests are written in the comments
- the functions folder holds some repetitive functions that may be imported and used in multiple of the tests such as logging into xplor and searching a client in xplor

## How the GUI works:
- The GUI is created using the CustomTkinter library to make the UI simple and easy to expand
- The GUI runs on a thread and the selenium tests are run on another thread to ensure that the GUI does not freeze when the tests are running
- To communicate between the tests and the GUI which run on different threads, a queue is utilized to communicate test statuses when the test are complete
- When the queue is populated, it is detected by a function in the main.py which calls on another function to modify the textbox in the UI that holds the logs 

## How running tests works
- When the user clicks start test, the `start_tests()` method will run where it will get all the checkboxes that are selected and append them to a list. The function 
will then check that logins and passwords are inputted. If no test is selected or no login/password is inputted, an error will appear in the log. 
- If login details are provided and the tests are selected, the `run_next_test()` method will start in a new thread which will go through the test selection array and determine
what tests have to be run by matching the number in the test selection array to an if/elif statement. 
- Once a match has been found, the `start_thread()` method is called in a new thread which simulatenously starts the test in a new thread with the configurations provided by the GUI and
calls on the `check_queue()` method in aother thread to monitor the queue for when it's populated. 

## How to create a new test:
- Create a new file in the main directory and name the file using the convention used for the other tests
- Inside the file create a function (this function will hold the code to run the script). The function should normally take in a queue to communicate with the GUI, login information, and whether the headless option was selected
- Wrap all the code inside a try-except-finally block to handle errors such as when the browser is manually closed. Make sure to add `from selenium.common.exception import WebDriverException` as this will be the exception thrown when a browser is manually closed
- Write all the code for the test as you would normally do for a selenium test, but make sure to create try catch blocks for each part and log the results by appending a string of the result to a list 
- At the end of the script, make sure to close the driver and push the list of results to the Queue

In `main.py`, import your test function from your test file, modify the TestSelection class and add the following:
```
    # This is for adding a checkbox to the selection
    self.checkbox<number> = customtkinter.CTkCheckBox(self, text=<Test Name>)
    self.checkbox<number>.grid(row=<number>, column=0, padx=10, pady=10, sticky="w")
```
then modify the `run_next_task()` function to include your test
```
# This code will start the test and modify the logs box in the UI to confirm tests started
    elif task == <number you chose for the checkbox>:
        modify_log(self, ['Starting <name of your test>'])
        start_thread(self, <test function you imported>, email, password, headless)
```
finally in the `start_test_function()` inside the App class, add the following lines
```
# This code will check if a checkbox is selected and if so, it will append it to the test_selection list 
if self.test.checkbox<number you chose for the checkbox>.get() == 1:
    test_selection.append(<number you chose for the checkbox>)
```

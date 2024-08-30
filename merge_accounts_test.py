""" Merge Accounts Test
This script attempts to find two accounts and merge them.
This script will search for accounts in the client look up, so 2 existing clients should exist for this test
The code can also create 2 new clients, but that has been commented out
"""
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import os
import string
import random
from time import sleep
from threading import Thread
from selenium.webdriver.common.keys import Keys
from threading import Condition
from functions.create_client import create_client

def merge_test(queue, email, password, headless):
    """ This function runs the log test

    Parameters: 
    queue (Queue): Is the queue that allows the different threads to communicate with each other. Test statuses are pushed to the queue to show up in the GUI
    email (str): Is the email used to login to xplor
    password (str): Is the password used to login to xplor
    headless (bool): Is used to determine whether to run the test as headless or not

    Returns:
    None
    """
    results = []
    results.append("==Merge Accounts==")

    query = "Sereinn" # Search query for the client 

    # Uncomment if you want this test to create 2 identical clients before merging them
    # details = {
    #     "first_name": "Sereinnn",
    #     "last_name" : "Zhuuu",
    #     "gender" : "(F) Female",
    #     "birth_month" : "June",
    #     "birth_day" : "06",
    #     "birth_year" : "2004",
    #     "mailing_street" : "10 Dundas Street East",
    #     "city" : "Toronto",
    #     "province" : "Ontario",
    #     "country" : "Canada",
    #     "zip_code" : "M5B 2G9",
    #     "mobile_type" : "Work",
    #     "phone_number" : "(987) 654-3210",
    #     "medical_condition" : "Diabetic",
    #     "emergency_fname" : "mom",
    #     "emergency_lname" : "dog",
    #     "emergency_phone1" : "(555) 555-5555",
    #     "emergency_phone2" : "(555) 555-5555",
    #     "emergency_email" : "fake@fake.com"
    # }
    # results += create_client(driver, details)
    # results += create_client(driver, details)


    # Setup
    options = webdriver.ChromeOptions()
    if headless: # Check if the headless option was requested
        options.add_argument("--headless=new")
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    driver.get('https://cdnbeta.perfectmind.com')
    driver.maximize_window()

    # Login
    try:
        driver.find_element(By.ID, 'textBoxUsername').send_keys(email)
        driver.find_element(By.ID, 'textBoxPassword').send_keys(password)
        driver.find_element(By.ID, 'buttonLogin').click()
        element_to_hover_over = driver.find_element(By.XPATH, "/html/body/div[5]/div[1]/table/tbody/tr[2]/td[1]/div/div/ul/li[1]")
    except:
        results.append("Unable to login with credentials")
        driver.close()
        queue.put(results)
    
    try:
        # Search by name, phone number, and email using search bar
        search_1 = driver.find_element(By.ID, "criteria")
        search_1.send_keys(query)
        search_1.send_keys(Keys.RETURN) 

        # Get Search Results and Select the first two entries by clicking on their checkboxes
        driver.implicitly_wait(5)
        checkboxes = driver.find_elements(By.CSS_SELECTOR, "input[type='checkbox'][class='row-checkbox xpl-checkbox']")
        checkboxes[0].click()
        checkboxes[1].click()
    except:
        results.append("Error with searching and choosing top two entries")

    # Attempt to merge accounts. Hover over the menu and then click merge contacts
    try:
        three_menu = driver.find_element(By.CSS_SELECTOR, "#customButtonsContainerDiv > #btnNav > ul[class='k-widget k-reset k-header k-menu k-menu-horizontal'][role='menubar']") 
        ActionChains(driver).move_to_element(three_menu).perform()
        driver.find_element(By.CSS_SELECTOR, "a#btnc5e767cd-49bc-4da7-9261-a4fff2ab1280").click()
        sleep(2)
        driver.find_element(By.CSS_SELECTOR, "#resultPopup > table > tbody > tr:nth-child(2) > td:nth-child(3) > a").click() # Click yes to merge clients
    except:
        results.append("Error navigating through merge process")
    # Check if clients merged from the popup and click "Okay" button
    try:
        driver.implicitly_wait(5)
        if driver.find_element(By.ID, "resultPopup").text == " All information has been merged to ":
            print("Done!")
        driver.find_element(By.ID, "okButton").click()
        results.append("✅ Merged Accounts")
    except:
        results.append("Error in merging accounts")
    driver.close()
    queue.put(results)







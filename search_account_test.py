""" Search Account Test
This script will run the tests to search for an account in the system by phone number, email, and account id
It will verify that contacts (clients under the account) and account schedules are viewable 
"""
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from time import sleep
from functions.search import search_client
from functions.create_client import create_client
import os
import string
import random

def search_account_test(queue,email,password, headless):
    """ This function tests the search client tasks under the respective UAT section of the spreadsheet

        Parameters: 
        queue (Queue): Is the queue that allows the different threads to communicate with each other. Test statuses are pushed to the queue to show up in the GUI
        email (str): Is the email used to login to xplor
        password (str): Is the password used to login to xplor
        headless (bool): Is used to determine whether to run the test as headless or not

        Returns:
        None
    """
    test_results = []
    test_results.append("==Search Account Test==")
    # Search queries, may update if profile dissapears 
    account_id = "AC-148960"
    phone_number = "(555) 555-5555"
    search_email = "bob.guy@sharklasers.com"

    # Setup
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)

    # Check if headless option was selected
    if headless:
        options.add_experimental_option('--headless=new')

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)

    driver.get('https://cdnbeta.perfectmind.com')
    driver.maximize_window()

    try:
        # Login to the profile
        driver.find_element(By.ID, 'textBoxUsername').send_keys(email)
        driver.find_element(By.ID, 'textBoxPassword').send_keys(password)
        driver.find_element(By.ID, 'buttonLogin').click()
        # Move cursor to navigate to Clients drop down, click Manage Account
        element_to_hover_over = driver.find_element(By.XPATH, "/html/body/div[5]/div[1]/table/tbody/tr[2]/td[1]/div/div/ul/li[1]/span[1]") 
    except:
        test_results.append("Error logging in")
        queue.put(test_results)
        driver.close()
    
    hover = ActionChains(driver).move_to_element(element_to_hover_over).perform()
    driver.find_element(By.XPATH, "/html/body/div[5]/div[1]/table/tbody/tr[2]/td[1]/div/div/ul/li[1]/div/ul/li[2]/a").click()

    try:
        # Search by Contact ID, phone number, and email using search bar
        search_client(driver, account_id, False)

        driver.implicitly_wait(5)
        search_client(driver, phone_number, False)

        driver.implicitly_wait(5)
        search_client(driver, search_email, True)
        test_results.append("✅ Searched by contact-id, phone number, email")
    except:
        test_results.append("Error searching")
        queue.put(test_results)
        driver.close()

    # Expand schedule
    try:
        driver.find_element(By.ID, "schedule-expand-link").click()
        test_results.append("✅ Schedule")
    except:
        test_results.append("Error with schedule")

    # Expand client tab to view contacts
    try:
        driver.find_element(By.XPATH, "/html/body/div[4]/div[3]/div[2]/div/div[4]/div[1]/div/div/div[1]/table/tbody/tr[2]/td/ul/li[2]").click()
        test_results.append("✅ Contacts")
    except:
        test_results.append("Error with view contacts")
    

    # Edit the name of an existing account
    new_name = "Guy Family 2"
    try:
        driver.find_element(By.ID, "editObject").click()
        account_name = driver.find_element(By.ID, 'fld_fa722c42-04b2-45db-aab8-3ddc286eaae4')
        account_name.clear()
        account_name.send_keys(new_name) 
        driver.find_element(By.ID, 'submitLinkVisible').click()
        test_results.append("✅Change account name")
    except:
        test_results.append("Unable to change account name")

    
    # Add new client to the account
    details = {
        "first_name": "Sereinnn",
        "last_name" : "Zhuuu",
        "gender" : "(F) Female",
        "birth_month" : "June",
        "birth_day" : "06",
        "birth_year" : "2004",
        "mailing_street" : "10 Dundas Street East",
        "city" : "Toronto",
        "province" : "Ontario",
        "country" : "Canada",
        "zip_code" : "M5B 2G9",
        "mobile_type" : "Work",
        "phone_number" : "(987) 654-3210",
        "medical_condition" : "Diabetic",
        "emergency_fname" : "mom",
        "emergency_lname" : "dog",
        "emergency_phone1" : "(555) 555-5555",
        "emergency_phone2" : "(555) 555-5555",
        "emergency_email" : "fake@fake.com"
    }
    driver.find_element(By.XPATH, "/html/body/div[4]/div[3]/div[2]/div/div[4]/div[1]/div/div/div[1]/table/tbody/tr[2]/td/ul/li[2]").click() 
    try: 
        create_client(driver, details)
        driver.implicitly_wait(5)
    except:
        test_results.append("Error adding new client to the account")

    # See family_modification_test to add existing client to the account/ remove client from the account 

    # Add Account Alert
    try:
        driver.find_element(By.XPATH, "/html/body/div[4]/div[3]/div[2]/div/div[4]/div[2]/div[3]/div[32]/div/div[1]/div/div[2]/a/span").click()
        driver.find_element(By.ID, "fld_9a453993-2ffe-8ebb-6767-d3565e0e465e").send_keys("test")
        driver.find_element(By.ID, "submitLinkVisible").click()
    except:
        test_results.append("Error with adding an alert")
    
    # Verify if alert is added 
    driver.find_element(By.CSS_SELECTOR, "a.back-button-link").click()
    alert_count_old = len(driver.find_elements(By.CLASS_NAME,"alert"))
    driver.find_element(By.XPATH, "/html/body/div[4]/div[3]/div[2]/div/div[4]/div[2]/div[3]/div[32]/div/div[1]/div/div[2]/a/span").click()
    driver.find_element(By.ID, "fld_9a453993-2ffe-8ebb-6767-d3565e0e465e").send_keys("test")
    driver.find_element(By.ID, "submitLinkVisible").click()
    driver.find_element(By.XPATH, "/html/body/div[4]/div[3]/div[2]/div/div[4]/div[2]/div[1]/a").click() 
    alert_count_new = len(driver.find_elements(By.CLASS_NAME,"alert"))
    if (alert_count_new == alert_count_old + 1):
        test_results.append("✅ Add alert")
    else:
        test_results.append("Error verifying added alert")


    # Run Account Statement 
    try:
        driver.find_element(By.XPATH, "/html/body/div[4]/div[3]/div[2]/div/div[4]/div[2]/div[2]/table/tbody/tr/td[1]/div[1]/div[3]/div/a[2]").click()
        test_results.append("✅ Run Account Statement")
    except:
        test_results.append("Error with account statement")  

    driver.close()
    queue.put(test_results)





  

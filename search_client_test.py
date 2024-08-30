""" Search Client Test
This script will run the tests to search for a client in the system by phone number, email, and name
It will verify that attendance, schedule, transactions, finance info, subsidy allocations, facility contracts, emails, documents, and alerts 
are viewable on the client's page
"""
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from time import sleep
from functions.search import search_client
import os
import string
import random

def search_client_test(queue,email,password, headless):
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
    test_results.append("==Search Client Test==")
    # Search queries, may update if profile dissapears 
    name = "Reigen Arataka"
    phone_number = "555-555-5555"
    search_email = "reigen.arataka@sharklasers.com"

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
        # Move cursor to navigate to Clients drop down on navbar, click manage clients
        element_to_hover_over = driver.find_element(By.XPATH, "/html/body/div[5]/div[1]/table/tbody/tr[2]/td[1]/div/div/ul/li[1]")
    except:
        test_results.append("Error logging in")
        queue.put(test_results)
        driver.close()
    
    hover = ActionChains(driver).move_to_element(element_to_hover_over).perform()
    driver.find_element(By.XPATH, "/html/body/div[5]/div[1]/table/tbody/tr[2]/td[1]/div/div/ul/li[1]/div/ul/li[1]/a").click()

    try:
        # Search by name, phone number, and email using search bar
        search_client(driver, name, False)

        driver.implicitly_wait(5)
        search_client(driver, phone_number, False)

        driver.implicitly_wait(5)
        search_client(driver, search_email, True)
        test_results.append("✅ Searched by phone, name, email")
    except:
        test_results.append("Error searching")
        queue.put(test_results)
        driver.close()

    '''
    note that the following code attempts to locate the respective fields on the client page using the numbered ids, if there are any new fields on the client page, the IDs may be altered and thus 
    may need updating
    '''
    #expand schedule
    try:
        driver.find_element(By.ID, "schedule-expand-link").click()
        test_results.append("✅ Schedule")
    except:
        test_results.append("Error with schedule")

    #expand contracts. This one searches by text. 
    try:
        driver.find_element(By.XPATH, "//*[contains(text(),'Facility Contracts')]").click()
        test_results.append("✅ Contracts")
    except:
        test_results.append("Error with contracts")

    #expand documents
    try:
        driver.find_element(By.CSS_SELECTOR, "#viewAgreementDoc1 > div.subsection-header.with-new-button > div > div.expand-link > h2").click()
        test_results.append("✅ Documents")
    except:
        test_results.append("Error with Documents")

    #expand attendance
    try:
        driver.find_element(By.ID, "viewAttendance4").click()
        test_results.append("✅ Attendance")
    except:
        test_results.append("Error with attendance")

    #expand finance info
    try:
        driver.find_element(By.ID, "viewFinanceInfo5").click()
        test_results.append("✅ Finance Info")
    except:
        test_results.append("Error with finance info")

    #transactions
    try:
        driver.find_element(By.ID, "viewTransaction6").click()
        test_results.append("✅ Transactions")
    except:
        test_results.append("Error with transactions")

    #subsidy
    try:
        driver.find_element(By.ID, "viewSubsidyAllocation10").click()
        test_results.append("✅ Subsidy")
    except: 
        test_results.append("Error with subsidy")

    #email
    try:
        driver.find_element(By.ID, "viewSentEmailRecipient11").click()
        test_results.append("✅ Email")
    except:
        test_results.append("Error with email")

    #alerts
    try:
        driver.find_element(By.ID, "viewAlert12").click()
        test_results.append("✅ Alerts")
    except:
        test_results.append("Error with alerts")
    
    driver.close()
    queue.put(test_results)



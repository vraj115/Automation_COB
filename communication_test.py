""" Communication Test
This script checks the following tests:
Activating consent emails, sending emails from client profiles, and reviewing email tab 
"""
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from functions.login import login
from time import sleep
from functions.search import search_client
import os
import string
import random
from queue import Queue
import time

def communication_test(queue, email, password, headless):
    """ This function runs the communication tests

    Parameters:
    queue: Is the queue that allows the different threads to communicate with each other. Test statuses are pushed to the queue to show up in the GUI
    email (str): Is the email used to login to Xplor
    password (str): Is the password used to login to Xplor
    headless (bool): Is used to determine whether to run the test as headless or not
    """
    
    # Setup
    test_results = []
    test_results.append("==Document Test==")
    options = webdriver.ChromeOptions()
        
    # Check if headless option selected
    if headless:
        options.add_argument("--headless=new")

    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)

    driver.get('https://cdnbeta.perfectmind.com')
    driver.maximize_window()

    # Login
    status = login(queue, driver, email, password, test_results)
    if not status: # If the status is false, end the test as there was an error 
        return

    ### Activate Consent Emails ###
    try:
        search_client(driver, "Reigen Arataka", True)
        three_menu = driver.find_element(By.CSS_SELECTOR, "#customButtonsContainerDiv > #btnNav > ul[class='k-widget k-reset k-header k-menu k-menu-horizontal'][role='menubar']") 
        ActionChains(driver).move_to_element(three_menu).perform()
        driver.find_element(By.CSS_SELECTOR, "a#btn1f9d3503-7f29-48c9-905a-da7ecfdfe405").click()
        sleep(2)
        driver.find_element(By.XPATH, "/html/body/div[34]/div[3]/a[1]")
        driver.find_element(By.XPATH, "/html/body/div[34]/div[3]/a[2]").click()
        test_results.append("✅ Activate Consent Emails")
    except:
        test_results.append("Error activating consent emails")

    ### Sending Email from Client Tab ###
    sent_email = False
    try:
        three_menu = driver.find_element(By.CSS_SELECTOR, "#customButtonsContainerDiv > #btnNav > ul[class='k-widget k-reset k-header k-menu k-menu-horizontal'][role='menubar']") 
        ActionChains(driver).move_to_element(three_menu).perform()
        driver.find_element(By.CSS_SELECTOR, "a#btn1dcbe9c3-2b88-4010-9dd6-d436a0e573f0").click()
        driver.find_element(By.CSS_SELECTOR, "input#Subject").send_keys("Test") # Enter a subject
        driver.find_element(By.ID, "emailSendButton").click() # Send email
        test_results.append("✅ Sending emails from Client")
        sent_email = True
    except:
        test_results.append("Error sending email from client tab")

    ### Reviewing Email Tab ##
    try:
        driver.back()
        if sent_email: # Need to go back an extra time if email was sent
            driver.back()
        driver.find_element(By.ID, "viewSentEmailRecipient11").click()
        test_results.append("✅ Review email tab")
    except:
        test_results.append("Error reviewing email tab")
    
    driver.close()
    queue.put(test_results)


    

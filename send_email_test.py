""" Send Email Test

This script will run the tests to send an email to a client in the system by email.
It will be sent from the recreation admin with a test message to ensure the email is appropriately sent through 

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
from selenium.common.exceptions import WebDriverException

def send_email_test(queue,email,password, headless):
    """ This function tests the send email tasks under the respective UAT section of the spreadsheet

        Parameters: 
        queue (Queue): Is the queue that allows the different threads to communicate with each other. Test statuses are pushed to the queue to show up in the GUI
        email (str): Is the email used to login to xplor
        password (str): Is the password used to login to xplor
        headless (bool): Is used to determine whether to run the test as headless or not

        Returns:
        None
    """
    try:
        
        test_results = []
        test_results.append("==Send email Test==")
        # Search queries, may update if profile dissapears 

        search_email = "test@sharklasers.com"
        subject_email = "test"
        message_email = "test"

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
            # Move cursor to navigate to Marketing drop down on navbar, click send emails
            element_to_hover_over = driver.find_element(By.XPATH, "/html/body/div[5]/div[1]/table/tbody/tr[2]/td[1]/div/div/ul/li[5]/span[1]")

        except:
            test_results.append("Error logging in")
            queue.put(test_results)
            driver.close()

        hover = ActionChains(driver).move_to_element(element_to_hover_over).perform()
        driver.find_element(By.XPATH, "/html/body/div[5]/div[1]/table/tbody/tr[2]/td[1]/div/div/ul/li[5]/div/ul/li[1]/a").click()

        try:
            # Search by email using search bar
            search_bar = driver.find_element(By.XPATH, "/html/body/div[4]/div[3]/div[2]/div/div[2]/div[6]/form/div[2]/table/tbody/tr[3]/td[2]/div/span/input")
            search_bar.clear()
            search_bar.send_keys(search_email)
            search_bar.send_keys(Keys.ENTER)
            driver.implicitly_wait(5)
            test_results.append("✅ Searched by email")

        except:
            test_results.append("Error searching")
            queue.put(test_results)


        try:
            # Send email through
            subject_bar = driver.find_element(By.XPATH, "/html/body/div[4]/div[3]/div[2]/div/div[2]/div[6]/form/div[2]/table/tbody/tr[4]/td[2]/input")
            subject_bar.clear()
            subject_bar.send_keys(subject_email)
            subject_bar.send_keys(Keys.ENTER)

            #message_field = driver.find_element(By.ID, "html_fld_8b0b7873-067b-4b5f-bbd5-f4f8500216dcContentHiddenTextarea")
            #html_fld_8b0b7873-067b-4b5f-bbd5-f4f8500216dc_contentIframe
            #message_field.clear()
            #message_field.send_keys(message_email)
            #message_field.send_keys(Keys.ENTER)


            driver.find_element(By.XPATH, "/html/body/div[4]/div[3]/div[2]/div/div[2]/div[1]/div/a[1]").click()
            driver.implicitly_wait(5)

            test_results.append("✅ Subject and message sent")

        except:
            test_results.append("Error sending email")
            queue.put(test_results)





    
        driver.close()

        

    except WebDriverException:
        queue.put(["Browser Exception"])

    finally:
        queue.put(test_results)




    
""" Create Account Test
This script creates a new account with the details specified below using the login provided
"""
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import WebDriverException
from time import sleep
from functions.create_client import create_client
from functions.login import login

def create_account_test(queue,email,password, headless):
    """ This function tests the search client tasks under the respective UAT section of the spreadsheet

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
        test_results.append("==Create Account Test==")

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

        status = login(queue, driver, email, password, test_results)
        if not status: # If the status is false, end the test as there was an error 
            return
        driver.find_element(By.XPATH, "/html/body/div[5]/div[1]/table/tbody/tr[2]/td[1]/div/div/ul/li[1]/div/ul/li[2]/a").click()

        
        # Create a family account
        try: 
            driver.find_element(By.ID, "newObject").click()
            driver.find_element(By.ID, "fld_fa722c42-04b2-45db-aab8-3ddc286eaae4").send_keys("Happy Test Family")
            driver.find_element(By.ID, 'submitLinkVisible').click()
            test_results.append("✅Create Family Account")
        except:
            test_results.append("Error with create family account")

        # Delete the account
        try: 

            driver.find_element(By.XPATH, "/html/body/div[4]/div[3]/div[2]/div/div[4]/div[2]/div[2]/table/tbody/tr/td[1]/div[1]/div[1]/a[2]").click()
            driver.find_element(By.ID, "confirmDeleteRecordDetailsButton").click() # confirm delete
            test_results.append("✅Delete Family Account")
        except:
            test_results.append("Error with delete account")

        # Create a new organization account
        try:  
            driver.find_element(By.ID, "newObject").click()
            driver.find_element(By.ID, "fld_fa722c42-04b2-45db-aab8-3ddc286eaae4").send_keys("Happy Organization")
            driver.find_element(By.XPATH, "/html/body/div[4]/div[3]/div[2]/div/table/tbody/tr/td/form/div[3]/div/div/div[1]/div[2]/table/tbody/tr/td[1]/table/tbody/tr[2]/td[2]/div/div[1]/span").click()
            driver.implicitly_wait(3) 
            driver.find_element(By.XPATH, ("/html/body/div[8]/div/div[2]/ul/li[2]")).click() # This may change to /html/body/div[9]/div/div[2]/ul/li[2]
            driver.find_element(By.XPATH, "/html/body/div[4]/div[3]/div[2]/div/table/tbody/tr/td/form/div[3]/div/div/div[1]/div[2]/table/tbody/tr/td[1]/table/tbody/tr[3]/td[2]/div/div[1]/span/span/span[1]").click()
            driver.find_element(By.XPATH, "/html/body/div[9]/div/div[2]/ul/li[20]").click()
            driver.find_element(By.ID, 'submitLinkVisible').click()
            test_results.append("✅Create Organization Account")
        except:
            test_results.append("Error with create organization account")
        
        # Close and output test results
        driver.close()
    except WebDriverException:
        queue.put(["Browser Exception"])
    finally:
        queue.put(test_results)




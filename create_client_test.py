""" Create Client Test
This script creates a client with the details specified below using the login provided
"""
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from time import sleep
from threading import Thread
from selenium.common.exceptions import WebDriverException
from functions.create_client import create_client
from functions.login import login
# Details of client to create
details = {
        "first_name": "Test",
        "last_name" : "Client",
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

def create_client_test(queue, email, password, headless):
        """ This tests whether the profile is able to create a client in xplor

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
                test_results.append("==Create Client Test==")
                options = webdriver.ChromeOptions()
                
                # Check if headless option selected
                if headless:
                        options.add_argument("--headless=new")

                options.add_experimental_option("detach", True)

                driver = webdriver.Chrome(options=options)
                driver.implicitly_wait(5)

                driver.get('https://cdnbeta.perfectmind.com')
                driver.maximize_window()

                # Login to the profile and then click create for a new client
                status = login(queue, driver, email, password, test_results)
                if not status: # If the status is false, end the test as there was an error 
                        return
                driver.find_element(By.XPATH, "/html/body/div[5]/div[1]/table/tbody/tr[2]/td[1]/div/div/ul/li[1]/div/ul/li[1]/a").click()
                test_results += create_client(driver, details)

                # Create and send login, there are issues sometimes running this part of the script, so user may have to manually click the buttons to send login
                try:
                        driver.implicitly_wait(3) # Create login first
                        driver.find_element(By.ID, "btnc12a44f4-6224-49b8-8747-d43444d48e47").click()
                        driver.implicitly_wait(3)
                        driver.find_element(By.ID, "CreateLoginButton").click()
                        driver.implicitly_wait(3)
                        driver.find_element(By.XPATH, "/html/body/div[23]/div[3]/a[1]").click() # Confirm sending 
                        driver.implicitly_wait(3)
                        driver.find_element(By.CSS_SELECTOR, "li.success")
                        test_results.append("✅Sent Member Login")
                except:
                        test_results.append("Error sending login")
                driver.close()

        except WebDriverException:
                queue.put(["Browser Exception"])
        except Exception as e:
                # Handle any exception that occurs during the test
                queue.put(f"Error occurred: {e}")
        finally:
        # Make sure to close the driver regardless of whether an exception occurred
                #driver.close()
                queue.put(test_results) 


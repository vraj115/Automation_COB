""" Create Client
This script creates a client in xplor and is not the test. 
The create client function in this file will be called inside other scripts.
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
from threading import Condition

def create_client(driver, details):
    """ Creates Client in Xplor

    Parameters:
    driver: The instance of the webdriver inside the other script to use 
    details (dict): A dictionary of the details of the client that should be created

    Return:
    None
    """
    test_results = [] # Store statuses in results array 
    try:
        #click the new button
        driver.find_element(By.XPATH, "/html/body/div[4]/div[3]/div[2]/div[5]/table/tbody/tr[2]/td[2]/form/div/table/tbody/tr/td/table/tbody/tr/td/a").click()

        #create random string for email
        letters = string.ascii_lowercase
        email = ''.join(random.choice(letters) for i in range(10))
        email+="@sharklasers.com"

        # Name
        driver.find_element(By.ID, 'fld_a7edaedc-495c-419f-b979-90e12e32338b').send_keys(details["first_name"])
        driver.find_element(By.ID, 'fld_23d93e7c-9485-4b5a-a817-7ffccc6e32b7').send_keys(details["last_name"])
        test_results.append("✅Entered Name")

        # Gender
        select_gender = Select(driver.find_element(By.ID, 'fld_8ebff50b-1cf4-4cc3-897a-49cb30dd55d9'))
        select_gender.select_by_visible_text(details["gender"])
        test_results.append("✅Selected Gender")

        # Birth date
        select_birth_month = Select(driver.find_element(By.ID, 'fld_fb344d3d-4a2d-43d1-9b56-b31b4a76a722-month'))
        select_birth_month.select_by_visible_text(details["birth_month"])
        driver.find_element(By.ID, 'fld_fb344d3d-4a2d-43d1-9b56-b31b4a76a722-day').send_keys(details["birth_day"])
        driver.find_element(By.ID, 'fld_fb344d3d-4a2d-43d1-9b56-b31b4a76a722-year').send_keys(details["birth_year"])
        test_results.append("✅Inputted Birthdate")

        # Address
        driver.find_element(By.ID, 'fld_2938a4be-93fa-4059-b782-6119263d6190-street').send_keys(details["mailing_street"])
        driver.find_element(By.ID, 'fld_2938a4be-93fa-4059-b782-6119263d6190-city').send_keys(details["city"])
        select_country = Select(driver.find_element(By.ID, 'fld_2938a4be-93fa-4059-b782-6119263d6190-country'))
        select_country.select_by_visible_text(details["country"])
        select_province = Select(driver.find_element(By.ID, 'fld_2938a4be-93fa-4059-b782-6119263d6190-province'))
        select_province.select_by_visible_text(details["province"])
        driver.execute_script(f"arguments[0].value = '{details["zip_code"]}';", driver.find_element(By.ID, 'fld_2938a4be-93fa-4059-b782-6119263d6190-postal-code'))
        test_results.append("✅Inputted Address")

        # Medical Condition
        driver.find_element(By.ID, "fld_5373c414-93a3-44fc-b5a6-a412df945e39").send_keys(details["medical_condition"])
        test_results.append("✅Inputted Medical Condition")

        # Phone Number
        driver.execute_script(f"arguments[0].value = '{details["phone_number"]}';", driver.find_element(By.ID, 'c2ea77c1-8293-4b86-9a9c-976daeae4832'))
        test_results.append("✅Inputted Phone Number")

        # Email Address
        driver.find_element(By.ID, "6f460e9b-d8df-4ae1-81ac-a8aa45fb3a5e").send_keys(email)
        test_results.append("✅Inputted email address")

        #emergency contact
        driver.find_element(By.ID, "fld_a9246d76-79e8-4dfa-9410-9de2deb5492c").send_keys(details["emergency_fname"])
        driver.find_element(By.ID, "fld_a6eb4c22-314c-4f7e-b322-85b4448cd33c").send_keys(details["emergency_lname"])
        driver.execute_script(f"arguments[0].value = '{details["emergency_phone1"]}';", driver.find_element(By.ID, '4973a506-299a-4b53-9ede-531c62f66c0c'))
        driver.execute_script(f"arguments[0].value = '{details["emergency_phone2"]}';", driver.find_element(By.ID, 'e1ed7004-f8bd-4a27-a6be-c82610e715a4'))
        driver.find_element(By.ID, "1bfef5bd-f79e-4204-85b5-e92f20720dee").send_keys(details["emergency_email"])
        test_results.append("✅Inputted emergency contact")

        #profile picture
        upload = driver.find_element(By.ID, "img_browse_e3415ad2-31da-41df-a2d6-9c1d9a8445a3")
        upload_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "pfp.png"))
        upload.send_keys(upload_file)
        test_results.append("✅Added profile picture")

        #save
        driver.execute_script("window.scrollTo(0, 0)")
        save = driver.find_element(By.ID, 'submitLinkVisible')
        save.click()
        test_results.append("✅Saved successfully")

    except Exception as err:
        test_results.append(str(err))
    # Return the array
    return test_results

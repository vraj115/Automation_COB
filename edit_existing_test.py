""" Edit an existing client tests
This script tests that the profile is able to manage logins, change client statuses, change contact information,
record prevent access reasons and create alerts, and validate that the alerts pop up.
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from functions.login import login
from functions.search import search_client
import random
import time

# Defining the user we want to search and the values we want to update
search_value = "reigen.arataka@sharklasers.com"
house_number = random.randint(1,100)
mailing_street = str(house_number)+" Dundas Street East"
city = "Toronto"
province = "Ontario"
country = "Canada"
zip_code = "M5B 2G9"
phone = "(555) 555-5551"

def edit_existing(queue, email, password, headless):
    """Attempts the tests under the edit existing section of UAT spreadsheet

    Parameters:
    queue (Queue): Is the queue that allows the different threads to communicate with each other. Test statuses are pushed to the queue to show up in the GUI
    email (str): Is the email used to login to xplor
    password (str): Is the password used to login to xplor
    headless (bool): Is used to determine whether to run the test as headless or not

    Returns:
    None

    """
    try:
        results = []
        results.append("==Edit Existing Test==")

        # Setup for Chrome 
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)

        # Check if headless option was selected
        if headless:
            options.add_experimental_option("--headless=new")

        driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(5)

        driver.get('https://cdnbeta.perfectmind.com')
        driver.maximize_window()

        # Login
        status = login(queue, driver, email, password, results)
        if not status: # If the status is false, end the test as there was an error 
            return
        driver.find_element(By.XPATH, "/html/body/div[5]/div[1]/table/tbody/tr[2]/td[1]/div/div/ul/li[1]/div/ul/li[1]/a").click()

        try:
            # Search for the defined user and click into the first one
            search_client(driver, search_value, True)
        except:
            results.append("Unable to click on a user")

        try:
            # Access the Manage Login popup
            driver.implicitly_wait(5)
            driver.find_element(By.ID, "btnc12a44f4-6224-49b8-8747-d43444d48e47").click()
            results.append("✅Able to Manage Login")
        except:
            results.append("Unable to Manage Login")

        # Check if buttons are clickable by checking if there is a disabled property on the buttons. This part assumes that the user's online login has been fully setup.
        driver.implicitly_wait(3)
        if driver.find_element(By.ID, "CreateLoginButton").is_enabled():
            results.append("✅Able to click Create")
        else:
            results.append("Cannot click Create")

        if driver.find_element(By.ID, "ResetLoginButton").is_enabled():
            results.append("✅Able to click Reset")
        else:
            results.append("Cannot click Reset")

        if driver.find_element(By.ID, "DeactivateLoginButton").is_enabled():
            results.append("✅Able to click Deactivate")
        else:
            results.append("Cannot click Deactivate")

        if driver.find_element(By.ID, "ActivateLoginButton").is_enabled():
            results.append("✅Able to click Activate")
        else:
            results.append("Cannot click Activate")

        # Close the menu 
        driver.implicitly_wait(3)
        driver.find_element(By.CSS_SELECTOR, "body > div.k-widget.k-window.k-display-inline-flex.xplor-popup.k-focused > div.k-window-titlebar.k-hstack > div > a").click()

        # Change contact information. Address is first changed and then Contact is changed.
        try:
            driver.find_element(By.ID, "editObject").click()
            driver.find_element(By.ID, 'fld_2938a4be-93fa-4059-b782-6119263d6190-street').send_keys(mailing_street)
            driver.find_element(By.ID, 'fld_2938a4be-93fa-4059-b782-6119263d6190-city').send_keys(city)
            select_country = Select(driver.find_element(By.ID, 'fld_2938a4be-93fa-4059-b782-6119263d6190-country'))
            select_country.select_by_visible_text(country)
            select_province = Select(driver.find_element(By.ID, 'fld_2938a4be-93fa-4059-b782-6119263d6190-province'))
            select_province.select_by_visible_text(province)
            driver.execute_script(f"arguments[0].value = '{zip_code}';",
                                driver.find_element(By.ID, 'fld_2938a4be-93fa-4059-b782-6119263d6190-postal-code'))

            driver.execute_script(f"arguments[0].value = '{phone}';",
                                driver.find_element(By.ID, 'c2ea77c1-8293-4b86-9a9c-976daeae4832'))
            results.append("✅Change contact information")
        except:
            results.append("Unable to change contact information")

        # Toggle prevent access and provide reason
        try:
            driver.execute_script("window.scrollTo(0, 0)")
            driver.find_element(By.ID, "fld_0c1f9471-5a8b-484c-8544-9702963fa42e").click()
            driver.find_element(By.ID, "fld_ac0296d4-4c15-4385-9d32-f9a3578a846f").send_keys("Broke into facility")
            results.append("✅ Toggle prevent access")
        except:
            results.append("Unable to toggle prevent access")

        # Add a custom ID
        try:
            driver.find_element(By.ID, "fld_1f7651f4-967c-4062-8896-de93c86b5572").send_keys("1111")
        except:
            results.append("Unable to add a custom ID")

        # Save changes
        try:
            driver.execute_script("window.scrollTo(0, 20)")
            save = driver.find_element(By.ID, 'submitLinkVisible')
            save.click()
        except:
            results.append("Error saving changes")

        # Add alert
        try:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            driver.find_element(By.CSS_SELECTOR, "a[data-objectid='e4f7a300-f9cb-49b6-93c8-557607055ac0']").click()
            driver.find_element(By.ID, "fld_9a453993-2ffe-8ebb-6767-d3565e0e465e").send_keys("test")
            driver.find_element(By.ID, "submitLinkVisible").click()
        except:
            results.append("Unable to add an alert")

        # Navigate back to client
        driver.find_element(By.CLASS_NAME, "back-button-link").click()

        # Count alerts. Alerts will include both access denied and alert red popups. 
        try:
            results.append(str(len(driver.find_elements(By.CLASS_NAME,"alert"))) + " alerts found")
        except:
            results.append("Error checking alerts and access denial")
        driver.close()
    except WebDriverException:
        queue.put(["Browser Exception"])
    finally:
        queue.put(results)

""" Logs Test
This file runs the automated Logs Tests for the conditions listed in the UAT spreadsheet
Creating a log, viewing a client logs, and deleting client logs will be done 
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from functions.login import login
from functions.search import search_client

def log_test(queue, email, password, headless):
    """ This function runs the log test

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
        search_query = "Reigen Arataka"
        results.append("==Log Test==")

        # Setup
        options = webdriver.ChromeOptions()
                
        # Check if headless option selected
        if headless:
            options.add_argument("--headless=new")
        options.add_experimental_option("detach", True)
        driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(5)
        driver.get('https://cdnbeta.perfectmind.com')
        driver.maximize_window()

        # Try logging in with credentials 
        try:
            login(queue, driver, email, password, results)
        except:
            results.append("Unable to login with credentials")
            driver.close()
            queue.put(results)

        # Navigate to the search bar and search for a client and click into the first profile
        try:
            search_client(driver, search_query, True)
        except:
            results.append("Error searching and clicking into profile")

        # Attempt to find logs
        try:
            driver.find_element(By.ID, "viewActivity2").click()
            results.append("✅ Found Logs")
        except:
            results.append("Unable to find logs")
        
        # Attempt to create log
        try:
            driver.find_element(By.CSS_SELECTOR, "a[title='New Log'][id='newObject']").click()
        except:
            results.append("Unable to click New Log button")

        # Populate Logs
        try:
            driver.find_element(By.ID, "fld_d15ef345-2bf0-44f7-b26d-c600bd129302").send_keys("Test") # Subject
            driver.find_element(By.ID, "fld_a540b089-d726-4a10-847b-21b123d2d8a5").send_keys("Test") # Details
            driver.find_element(By.ID, "fld_954d6e1d-426d-4f85-981f-127da92f6f40").send_keys("123") # Course ID
        except:
            results.append("Unable to populate fields")

        # Save
        try:
            driver.execute_script("window.scrollTo(0, 0)")
            driver.find_element(By.CSS_SELECTOR, '#builtInButtons > div > #submitLink').click()
            results.append("✅ Successfully Created Logs")
        except:
            results.append("Unable to save")

        # End script
        driver.close()
    except WebDriverException:
        queue.put(["Browser Exception"])
    finally:
        queue.put(results)
    

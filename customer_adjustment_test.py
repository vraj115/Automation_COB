""" Customer Adjustment Test
This file runs the customer adjustment test for the conditions listed in the UAT spreadsheet
Granting a credit with customer adjustment and charging and client with adjustment will be tested.
"""
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import WebDriverException
from time import sleep
from functions.search import search_client
from functions.login import login

def adjustment_test(queue, email, password, headless):
    """ This function runs the customer adjustment test

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
        results.append("==Customer Adjustment Test==")

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

        # Login to the profile and then click create for a new client
        status = login(queue, driver, email, password, results)
        if not status: # If the status is false, end the test as there was an error 
            return

        # Navigate to a random profile and click on first instance
        try:
            search_client(driver, "Reigen Arataka", True)
        except:
            results.append("Error searching for the client.")
            driver.close()
            queue.put(results)

        # Navigate to the nav bar and hover over more 
        try:
            element_to_hover_over = driver.find_element(By.XPATH, "//*[@id='ApplicationMenu']/li[6]")
            hover = ActionChains(driver).move_to_element(element_to_hover_over).perform()
            
            # Hover over bookkeeping which is the second option 
            # Selenium is buggy and may sometimes hover over the wrong item
            menu_dropdown = driver.find_elements(By.CSS_SELECTOR,"#ApplicationMenu > li.k-item.more-btn.k-state-default.k-menu-item.k-last > div > ul > li")
            reports = menu_dropdown[0]
            ActionChains(driver).move_to_element(reports).perform()
            book_keeping = menu_dropdown[1]
            ActionChains(driver).move_to_element_with_offset(book_keeping, 1,1 ).perform()
            sleep(2)

            # Select Customer Adjustment which is the 5th option (may need to update )
            book_keeping_options = book_keeping.find_element(By.CSS_SELECTOR, "div > ul")
            choices = book_keeping_options.find_elements(By.CSS_SELECTOR, "li[role='menuitem']")
            choices[4].click()
        except:
            results.append("Error navigating to customer adjustments")
            driver.close()
            queue.put(results)

        # Wait for the processing popup menu to appear
        sleep(5)

        # Pick the station 
        try:
            counter = 0
            while True:
                drops = driver.find_elements(By.ID, "assignLocationStationPicker") # Need this while loop because the site has multiple elements with the ID 
                try:
                    drop = Select(drops[counter])
                    drop.select_by_index(1)
                    break
                except:
                    counter = counter+1

            # Need this while loop as well due to the multiple elements with the same selector 
            parents = driver.find_elements(By.CSS_SELECTOR, "div.assign-station-buttons")
            counter_2 = 0
            while True:
                try:
                    station_buttons = parents[counter_2].find_elements(By.TAG_NAME, "button")
                    station_buttons[0].click()
                    break
                except:
                    counter_2 = counter_2+1

            # Need this while loop due to multiple instances of the button of the same selector
            choose_buttons = driver.find_elements(By.CSS_SELECTOR,"div.assign-location-actions > button")
            counter_3 = 0
            while True:
                try:
                    choose_buttons[counter].click()
                    break
                except:
                    counter_3 = counter_3+1
        except:
            results.append("Error selecting POS")
            driver.close()
            queue.put(results)
        
        sleep(1)

        # Fill in fields
        try:
            # Select Adjustment Type
            driver.find_element(By.XPATH, "//*[@id='adjWindow']/table/tbody/tr[5]/td[2]/span").click()
            driver.find_element(By.CSS_SELECTOR, "#custAdjustmentType_listbox > li:nth-child(2)").click()

            # Annotation
            driver.find_element(By.CSS_SELECTOR, "textarea#annotation").send_keys("Test")
            sleep(5)

            # Click add a GL Account
            driver.find_element(By.CSS_SELECTOR, "span[title='Add GL Account']").click()

            # Input value
            driver.find_element(By.XPATH, "//*[@id='adjWindow']/table/tbody/tr[7]/td[2]/ul/li/span[2]/span/input[1]").send_keys(10)

            # Click Save
            driver.find_element(By.CSS_SELECTOR, "a.pm-save-button").click()
            results.append("✅ Added a customer adjustment")
        except:
            results.append("Error filling in adjustment details")
            driver.close()
            queue.put(results)

        sleep(5)
        
        # End script
        driver.close()
    except WebDriverException:
        queue.put(["Browser Exception"])
    finally:
        queue.put(results)
    

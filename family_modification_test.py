""" Family Modification

This script runs the Family Members tests - Add a family member to an existing client record
Remove family members and keep credits with family.
This test runs as long as it searches for an existing client in the beta site database. The search query can be updated.
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium import webdriver
from time import sleep
from functions.search import search_client
from functions.login import login
from selenium.common.exceptions import WebDriverException

def family_test(queue, email, password, headless):
    try:
        results = []
        results.append("==Family Test==")

        # Define what is going to be searched in the client search bar
        search_query = "Reigen Arataka"

        # Define Specifications for the New Client to be created
        name = "Rego"
        birth_day = 19
        birth_year = 1999

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

        # Navigate to search and search for client
        driver.find_element(By.XPATH, "/html/body/div[5]/div[1]/table/tbody/tr[2]/td[1]/div/div/ul/li[1]/div/ul/li[1]/a").click()

        # Search by name, phone number, and email using search bar
        try:
            search_client(driver, search_query, True)
        except:
            results.append("Error searching and clicking on profile")

        # Scroll on the left menu to the bottom and click add family member
        try:
            driver.implicitly_wait(3)
            add_family = driver.find_element(By.ID, "spnaddfamilymember-top")
            driver.execute_script('arguments[0].scrollIntoView(true);', add_family)
            add_family.click()

            # Click on New Contact to create a new client
            driver.find_element(By.ID, "spnaddnewcontact").click()
        except:
            results.append("Error adding a family member")

        # Fill out the details needed
        try:
            # First and name
            driver.find_element(By.ID, "fld_a7edaedc-495c-419f-b979-90e12e32338b").send_keys(name)

            # Birthday 
            driver.find_element(By.ID, 'fld_fb344d3d-4a2d-43d1-9b56-b31b4a76a722-day').send_keys(birth_day)
            driver.find_element(By.ID, 'fld_fb344d3d-4a2d-43d1-9b56-b31b4a76a722-year').send_keys(birth_year)

            # Phone Number
            driver.execute_script(f"arguments[0].value = '{"(555) 555-5555"}';", driver.find_element(By.ID, 'c2ea77c1-8293-4b86-9a9c-976daeae4832'))

            # Save
            sleep(1)
            driver.execute_script("window.scrollTo(0, 0);")
            save = driver.find_element(By.ID, 'submitLinkVisible').click()
            results.append("✅ Created a family member")
        except:
            results.append("Error saving deials of new family member")

        # Store current credit balance and then add to credit balance
        try:
            account_balance = driver.find_element(By.CSS_SELECTOR, "button.pm-balance-button").get_attribute("innerHTML")
            driver.find_element(By.CSS_SELECTOR, "button.pm-balance-button").click()
            sleep(0.5)
            driver.find_element(By.CSS_SELECTOR, "button#buyAccountCreditButton").click()
            driver.find_element(By.CSS_SELECTOR, "#containerBuyCreditPopup > div.amount-section > span.k-widget.k-numerictextbox > span > input.k-formatted-value.k-input").click()
            sleep(0.5)
            driver.find_element(By.CSS_SELECTOR, "#containerBuyCreditPopup > div.amount-section > span.k-widget.k-numerictextbox > span > input#buycreditamount").send_keys("10")
            driver.find_element(By.CSS_SELECTOR, "#containerBuyCreditPopup > div:nth-child(3) > button#btnbuycredit").click()
        except:
            results.append("Error buying credits")

        # Navigate through POS and purchase the credit using a cheque. When selecting a location, index 1 is 8 nelson. 
        try:
            sleep(5)
            drop = Select(driver.find_element(By.ID, "assignLocationStationPicker")) # Select a terminal location and choose it
            drop.select_by_index(1)
            parent = driver.find_element(By.CSS_SELECTOR, "div.assign-station-buttons")
            station_buttons = parent.find_elements(By.TAG_NAME,"button")
            station_buttons[0].click()
            driver.find_element(By.XPATH,"//button[text()='Choose']").click() 
            sleep(1)
            driver.find_element(By.XPATH,"//*[@id='quickPayCharge']").click() # Process Payment
            sleep(5)
            driver.find_element(By.CSS_SELECTOR, "button[id='7d895e5e-0c19-4389-9407-e3b18dc33277'][class='co2-checkout-payment-type']").click()
            driver.find_element(By.CSS_SELECTOR, "input[name='checkNumber']").send_keys(132)
            driver.find_element(By.CSS_SELECTOR, "button.co2-process-now").click()
            results.append("✅ Purchased Credits")
        except:
            results.append("Error processing POS")

        # Return to user to remove the family member 
        try:
            driver.find_element(By.CSS_SELECTOR, "div.pm-cgt-container > div > div.pm-cgt-content > div > div.pm-cgt-body-field.pm-cgt-larger.pm-cgt-strong > a").click()
            driver.implicitly_wait(3) # Scroll on the left menu to the bottom and click add family member
            driver.execute_script('arguments[0].scrollIntoView(true);', driver.find_element(By.ID, "spnaddfamilymember-top"))
            driver.find_element(By.CSS_SELECTOR,"#contactfamilysection > ul > li:nth-child(1) > span").click() # Select the family member to remove
            family = Select(driver.find_element(By.ID, "familyMembersDropDownList")) # Select the person to grant the credit to 
            family.select_by_index(1)
            driver.find_element(By.CSS_SELECTOR, "button#spnremovecontactfromfamily").click() # Click remove from family 
            results.append("✅ Removed Family Member")
        except:
            results.append("Error removing family member")
        driver.close()
    except WebDriverException:
        queue.put(["Browser Exception"])
        return
    finally:
        # Close the browser and add test results to queue to be displayed
        queue.put(results)

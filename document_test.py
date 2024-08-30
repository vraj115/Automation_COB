""" Document Test 
Tests to see if the following criteria from UAT testing are met:
Able to print membership agreement (under Membership tab), Review Documents tab, Delete client documents
and View Manage Documents from client drop-down 
"""
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from time import sleep
from functions.login import login
from functions.search import search_client

def document_test(queue, email, password, headless):
    """ This tests whether different aspects of document view can be used/clicked

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

        #Input the login for the profile you want to use
        status = login(queue, driver, email, password, test_results)
        if not status: # If the status is false, end the test as there was an error 
            return

        # Move navigate to Clients drop down on navbar, click manage clients
        driver.find_element(By.XPATH, "/html/body/div[5]/div[1]/table/tbody/tr[2]/td[1]/div/div/ul/li[1]/div/ul/li[1]/a").click()

        # Search for a client and click into the first one 
        search_client(driver, "Reigen Arataka", "True")

        ### Review Documents tab, Print Membership Agreement, and Delete Client Documents ###
        try:
            # Scroll to middle of page and click on the documents tab
            documents = driver.find_element(By.ID, "viewAgreementDoc1")
            driver.execute_script("arguments[0].scrollIntoView(true);", documents)
            sleep(1)
            driver.find_element(By.XPATH, "//*[@id='viewAgreementDoc1']/div[1]/div/div[1]/h2").click()

            # Find the Membership Agreement entry
            table = driver.find_element(By.CSS_SELECTOR, "#grdAgreementDoc2 > table")
            rows = table.find_elements(By.CLASS_NAME, "aoda_filter__Name")
            for x in rows: # Go through the Name column to find the membership agreement
                text = x.text
                words = text.split()
                for j in range(len(words)):
                    if words[j] ==  "Membership" and words[j+1] == "Agreement":
                        x.click()
            test_results.append("✅ Review Documents Tab")
        except:
            test_results.append("Error reviewing documents tab")

        # Check if able to print by looking for an embedded PDF element
        try:
            driver.find_element(By.TAG_NAME, "embed")
            test_results.append("✅ Able to print")
        except:
            test_results.append("Error printing")

        # Check to see if delete button is available on document
        try:
            driver.find_element(By.CSS_SELECTOR, "a[title='Delete']")
            test_results.append("✅ Able to delete documents")
        except:
            test_results.append("Unable to delete documents")

        # See if 'Manage Documents' is accessible from the clients drop-down 
        try:
            element_to_hover_over_2 = driver.find_element(By.XPATH, "/html/body/div[4]/div[1]/table/tbody/tr[2]/td[1]/div/div/ul/li[1]")
            ActionChains(driver).move_to_element(element_to_hover_over_2).perform()
            driver.find_element(By.XPATH, "/html/body/div[4]/div[1]/table/tbody/tr[2]/td[1]/div/div/ul/li[1]/div/ul/li[3]/a").click()
        except:
            test_results.append("Error trying to access 'Manage Documents'")

        driver.close()
    except WebDriverException:
        queue.put(["Browser Exception"])
    finally:
        queue.put(test_results)
    
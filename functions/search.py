from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from time import sleep

def search_client(driver, query, click):
    """ This function searches for a client on Xplor and can click onto the first profile that pops up

    Parameters:
    driver: The selenium webdriver to perform the tasks
    query (str): The search query to put into the search bar
    click (Bool): Whether to click onto the first profile or not

    Returns:
    None
    """
    search = driver.find_element(By.ID, "criteria")
    search.clear() # Clear the search bar in case additional searches are made
    search.send_keys(query)
    search.send_keys(Keys.RETURN) 
    # Click into the first profile 
    if click:
        driver.implicitly_wait(3)
        rows = driver.find_elements(By.CSS_SELECTOR, "#gridRecords > table > tbody > tr")
        sleep(2)
        rows[0].click()
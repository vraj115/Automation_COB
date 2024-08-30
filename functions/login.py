from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

def login(queue, driver, email, password, test_results):
    """ This function holds the code needed to login to the Xplor website 

    Parameters:
    queue (Queue): holds the statuses of the current test
    driver: The instance of the webdriver that we want to use from the other script
    email (str): The email used to login 
    password (str): The password used to login
    test_results (list of str): The list of test results that will be sent to the GUI  
    """
    try:
        driver.find_element(By.ID, 'textBoxUsername').send_keys(email)
        driver.find_element(By.ID, 'textBoxPassword').send_keys(password)
        driver.find_element(By.ID, 'buttonLogin').click()
        element_to_hover_over = driver.find_element(By.XPATH, "/html/body/div[5]/div[1]/table/tbody/tr[2]/td[1]/div/div/ul/li[1]") # Should be able to locate if logged in successfully 
        ActionChains(driver).move_to_element(element_to_hover_over).perform()
        return True
    except:
        test_results.append("Unable to login with credentials")
        driver.close()
        queue.put(test_results)
        return False
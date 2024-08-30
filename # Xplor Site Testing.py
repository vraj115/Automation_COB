# Xplor Site Testing
# import webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


# create webdriver object
driver = webdriver.Firefox()

driver.get("https://cityofbramptontest.perfectmind.com/Contacts/MemberRegistration/MemberSignIn?returnUrl=%2FContacts%2FContact")
email_input = driver.find_element(By.XPATH, "//*[@id='textBoxUsername']")
password_input = driver.find_element(By.XPATH, "//*[@id='textBoxPassword']")
login_button = driver.find_element(By.XPATH, "//*[@id='buttonLogin']")

email_input.click()
email_input.send_keys("bramptontest")

password_input.click()
password_input.send_keys("Brampton123")

login_button.click()




#driver.quit()

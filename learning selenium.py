# import webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


# create webdriver object
driver = webdriver.Chrome()

# get google
driver.get("https://www.google.com/")
search_input = driver.find_element(By.NAME, "q")
#search_input.click()
search_input.send_keys("nba scores")
search_input.send_keys(Keys.ENTER)
images = driver.find_element(By.XPATH, "//*[@id='hdtb-sc']/div/div[1]/div[1]/div/div[3]").click()



#driver.quit()
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
link = "http://suninjuly.github.io/file_input.html"

try:
    browser = webdriver.Chrome()
    browser.get(link)

    input = browser.find_element(By.TAG_NAME, "input")
    input.send_keys("Ivan")

    input = browser.find_element(By.NAME, "lastname")
    input.send_keys("Petrov")

    input = browser.find_element(By.NAME, "email")
    input.send_keys("pavelpankov12@mail.ru")

    input = browser.find_element(By.XPATH, "//input[@type='file']")
    
    current_dir = os.path.abspath(os.path.dirname(__file__))    
    file_path = os.path.join(current_dir, 'file.txt')           
    input.send_keys(file_path)

    button = browser.find_element(By.CSS_SELECTOR, "button.btn")
    button.click()
finally:
    time.sleep(10)
    browser.quit()
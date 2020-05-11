from selenium import webdriver
from selenium.webdriver.common.by import By
from pages.home.login_page import LoginPage
import unittest

class LoginTests(unittest.TestCase):
    def testLogin(self):
        base_url = "https://learn.letskodeit.com/p/practice"
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.implicitly_wait(5)
        driver.get(base_url)

        lp = LoginPage(driver)
        lp.login('test@email.com', "abcabc")

        gravatar = driver.find_element_by_xpath("//img[@class='gravatar']")
        if gravatar is not None:
            print("Login Successful")
        else:
            print("Login Failed")

loginTest = LoginTests()
loginTest.testLogin()
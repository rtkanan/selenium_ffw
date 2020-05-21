from selenium import webdriver
from pages.home.login_page import LoginPage
import unittest

class LoginTests(unittest.TestCase):
    base_url = "https://letskodeit.teachable.com/"
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(5)
    driver.get(base_url)
    lp = LoginPage(driver)

    def testInvalidLogin(self):
        self.lp.login()

        result = self.lp.verifyLoginFailure()
        assert result == True

    def testValidLogin(self):
        self.lp.login('test@email.com', "abcabc")

        gravatar = self.lp.verifyLoginSuccessful()
        assert gravatar == True
    

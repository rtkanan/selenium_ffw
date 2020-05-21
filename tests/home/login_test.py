from selenium import webdriver
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

        gravatar = lp.verifyLoginSuccessful()
        assert gravatar == True

        driver.quit()

if __name__ == "__main__":
    loginTest = LoginTests()
    loginTest.testLogin()

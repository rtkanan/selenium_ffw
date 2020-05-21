from selenium.webdriver.common.by import By
from base.selenium_webdriver import SeleniumDriver
import utilities.custom_logger as logger
import logging

class LoginPage(SeleniumDriver):
    log = logger.customLogger(logging.DEBUG)

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
    
    # Locators
    _login_link = "//a[@href='/sign_in']"
    _email_field = "user_email"
    _pwd_field = "user_password"
    _login_button = "//input[@value='Log In']"
    _gravatar = "//img[@class='gravatar']"

    # Actions
    def clickLoginLink(self):
        self.clickElement(self._login_link, "xpath")
    
    def enterEmail(self, email):
        self.sendKeys(email, self._email_field)
    
    def enterPassword(self, pwd):
        self.sendKeys(pwd, self._pwd_field)
    
    def clickLoginButton(self):
        self.clickElement(self._login_button, "xpath")

    # Functionality
    def login(self, username, password):
        self.clickLoginLink()
        self.enterEmail(username)
        self.enterPassword(password)
        self.clickLoginButton()

    def verifyLoginSuccessful(self):
        gravatar = self.isElementPresent(self._gravatar, "xpath")
        return gravatar
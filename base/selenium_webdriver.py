from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions
from traceback import print_stack

class SeleniumDriver():

    def __init__(self, driver):
        self.driver = driver

    def getByType(self, locatorType):
        locatorType = locatorType.lower()
        if locatorType == "id":
            return By.ID
        elif locatorType == "name":
            return By.NAME
        elif locatorType == "xpath":
            return By.XPATH
        elif locatorType == "css":
            return By.CSS_SELECTOR
        elif locatorType == "class":
            return By.CLASS_NAME
        elif locatorType == "link":
            return By.LINK_TEXT
        else:
            print("Locator type " + locatorType + " not correct/supported")
        return False

    def getElement(self, locator, locatorType="id"):
        element = None
        try:
            locatorType = locatorType.lower()
            byType = self.getByType(locatorType)
            element = self.driver.find_element(byType, locator)
            print(f"Element found with locator: {locator} and locatorType: {locatorType}")
        except:
            print(f"Element not found with locator: {locator} and locatorType: {locatorType}")
        return element
    
    def clickElement(self, locator, locatorType="id"):
        try:
            element = self.getElement(locator, locatorType)
            element.click()
            print(f"Clicked on the identified element with locator: {locator} and locatorType: {locatorType}")
        except:
            print(f"Cannot click on the element with locator: {locator} and locatorType: {locatorType}")
            print_stack()
    
    def sendKeys(self, data, locator, locatorType="id"):
        try:
            element = self.getElement(locator, locatorType)
            element.clear()
            element.send_keys(data)
            print(f"Entered data in the element with locator: {locator} and locatorType: {locatorType}")
        except:
            print(f"Not able to enter the data in the element with locator: {locator} and locatorType: {locatorType}")
            print_stack()

    # Todo this can be merged with getElement itself
    def isElementPresent(self, locator, locatorType="id"):
        try:
            element = self.getElement(locator, locatorType)
            if element is not None:
                print(f"Element found with locator: {locator} and locatorType: {locatorType}")
                return True
            else:
                print(f"Element not found with locator: {locator} and locatorType: {locatorType}")
                return False
        except:
            print(f"Element not found with locator: {locator} and locatorType: {locatorType}")
            return False

    def elementPresenceCheck(self, locator, byType):
        try:
            elementList = self.driver.find_elements(byType, locator)
            if len(elementList) > 0:
                print("Element Found")
                return True
            else:
                print("Element not found")
                return False
        except:
            print("Element not found")
            return False
    
    def waitForElement(self, locator, locatorType="id", timeout=10, pollFrequency=0.5):
        element = None
        try:
            byType = self.getByType(locatorType)
            print("Waiting for maximum :: " + str(timeout) +
                          " :: seconds for element to be clickable")
            wait = WebDriverWait(self.driver, timeout=timeout, poll_frequency=pollFrequency,
                                 ignored_exceptions=[exceptions.NoSuchElementException,
                                                     exceptions.ElementNotVisibleException,
                                                     exceptions.ElementNotSelectableException])
            element = wait.until(EC.element_to_be_clickable((byType, locator)))
            print("Element appeared on the web page")
        except:
            print("Element not appeared on the web page")
            print_stack()
        return element

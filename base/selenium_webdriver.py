from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions
from traceback import print_stack
import utilities.custom_logger as logger
import logging
import time
import os

class SeleniumDriver():
    log = logger.customLogger(logging.DEBUG)

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
            self.log.info("Locator type " + locatorType + " not correct/supported")
        return False

    def getElement(self, locator, locatorType="id"):
        element = None
        try:
            locatorType = locatorType.lower()
            byType = self.getByType(locatorType)
            element = self.driver.find_element(byType, locator)
            self.log.info(f"Element found with locator: {locator} and locatorType: {locatorType}")
        except:
            self.log.error(f"### Exception occurred: Element not found with locator: {locator} and locatorType: {locatorType}")
        return element
    
    def getElementList(self, locator, locatorType="id"):
        elements = None
        try:
            locatorType = locatorType.lower()
            byType = self.getByType(locatorType)
            elements = self.driver.find_elements(byType, locator)
            self.log.info(f"Elements found with locator: {locator} and locatorType: {locatorType}")
        except:
            self.log.error(f"### Exception occurred: Elements not found with locator: {locator} and locatorType: {locatorType}")
        return elements
    
    def clickElement(self, locator="", locatorType="id", element=None):
        try:
            if locator:
                element = self.getElement(locator, locatorType)
            element.click()
            self.log.info(f"Clicked on the identified element.")
        except:
            self.log.error(f"### Exception occurred: Cannot click on the element")
            # print_stack()
    
    def sendKeys(self, data, locator="", locatorType="id", element=None):
        try:
            if locator:
                element = self.getElement(locator, locatorType)
            element.clear()
            element.send_keys(data)
            self.log.info(f"Entered data in the element with locator: {locator} and locatorType: {locatorType}")
        except:
            self.log.error(f"Not able to enter the data in the element with locator: {locator} and locatorType: {locatorType}")
            # print_stack()
    
    def getText(self, locator="", locatorType="id", element=None, info=""):
        try:
            if locator:
                element = self.getElement(locator, locatorType)
            text = element.text
            self.log.debug(f"Length of text {str(len(text))}")
            if len(text) == 0:
                text = element.get_attribute("innerText")
            self.log.info(f"Fetched text for element {info} is: '{text}'")
            text = text.strip()
        except:
            self.log.error(f"### Exception occurred: Failed to get text on element {info}")
            print_stack()
            text = None
        return text

    # Todo: Check the possibility merging this funtion with getElement
    def isElementPresent(self, locator="", locatorType="id", element=None):
        try:
            if locator:
                element = self.getElement(locator, locatorType)
            if element is not None:
                self.log.info(f"Element found with locator: {locator} and locatorType: {locatorType}")
                return True
            else:
                self.log.info(f"Element not found with locator: {locator} and locatorType: {locatorType}")
                return False
        except:
            self.log.error(f"### Exception occurred: Element not found")
            return False
    
    def isElementDisplayed(self, locator="", locatorType="id", element=None):
        isDisplayed = False
        try:
            if locator:
                element = self.getElement(locator, locatorType)
            if element is not None:
                isDisplayed = element.is_displayed()
                self.log.info(f"Element is displayed with locator: {locator} and locatorType: {locatorType}")
            else:
                self.log.info(f"Element is not displayed with locator: {locator} and locatorType: {locatorType}")
            return isDisplayed
        except:
            self.log.error(f"### Exception occurred: Element not found")
            return False

    def elementPresenceCheck(self, locator, byType):
        try:
            elementList = self.driver.find_elements(byType, locator)
            if len(elementList) > 0:
                self.log.info("Element Found")
                return True
            else:
                self.log.info("Element not found")
                return False
        except:
            self.log.error("### Exception Occurred: Element not found")
            return False
    
    def waitForElement(self, locator, locatorType="id", timeout=10, pollFrequency=0.5):
        element = None
        try:
            byType = self.getByType(locatorType)
            self.log.info("Waiting for maximum :: " + str(timeout) +
                          " :: seconds for element to be clickable")
            wait = WebDriverWait(self.driver, timeout=timeout, poll_frequency=pollFrequency,
                                 ignored_exceptions=[exceptions.NoSuchElementException,
                                                     exceptions.ElementNotVisibleException,
                                                     exceptions.ElementNotSelectableException])
            element = wait.until(EC.element_to_be_clickable((byType, locator)))
            self.log.info("Element appeared on the web page")
        except:
            self.log.error("### Exception Occurred: Element not appeared on the web page")
            # print_stack()
        return element
    
    def getTitle(self):
        """
        Fetches the title of the current web page
        """
        return self.driver.title
    
    def takeScreenshot(self, fileNamePrefix):
        """
        Takes screenshot of the current web page
        """
        currentTime = str(round(time.time() * 1000))
        fileName = f"{fileNamePrefix}_{currentTime}.png"
        cwd = os.path.dirname(__file__)
        screenshotPath = os.path.join(cwd, "..\\screenshots")
        screenshotFilePath = os.path.join(screenshotPath, fileName)

        try:
            if not os.path.exists(screenshotPath):
                os.makedirs(screenshotPath)
            self.log.info(f"Save the screenshot: {screenshotFilePath}")
            self.driver.save_screenshot(screenshotFilePath)
        except:
            self.log.error(f"### Exception Occurred: Not able save the screenshot: {screenshotFilePath}")
            # print_stack()
    
    def scroll(self, direction="down"):
        if direction.lower() == "down":
            # Scroll down
            self.driver.execute_script("window.scrollBy(0, 1000);")
        
        if direction.lower() == "up":
            # Scroll up
            self.driver.execute_script("window.scrollBy(0, -1000);")
    
    def switch_to_frame(self, locator=None):
        # Swich to iframe
        try:
            self.driver.switch_to.frame(locator)
        except:
            self.log.error(f"### Exception Occurred: Not able to identify the iframe with locator {locator}")
    
    def switch_to_default(self):
        # Swith to default content from any iframe
        self.driver.switch_to.default_content()
    
    def getElementAttributeValue(self, attribute, element=None, locator="", locatorType="id"):
        """
        Get value of the attribute of element

        Parameters:
            1. Required:
                1. attribute - attribute whose value to find

            2. Optional:
                1. element   - Element whose attribute need to find
                2. locator   - Locator of the element
                3. locatorType - Locator Type to find the element

        Returns:
            Value of the attribute
        Exception:
            None
        """
        if locator:
            element = self.getElement(locator=locator, locatorType=locatorType)
        value = element.get_attribute(attribute)
        return value

    def isEnabled(self, locator, locatorType="id", info=""):
        """
        Check if element is enabled

        Parameters:
            1. Required:
                1. locator - Locator of the element to check
            2. Optional:
                1. locatorType - Type of the locator(id(default), xpath, css, className, linkText)
                2. info - Information about the element, label/name of the element
        Returns:
            boolean
        Exception:
            None
        """
        element = self.getElement(locator, locatorType=locatorType)
        enabled = False
        try:
            attributeValue = self.getElementAttributeValue(element=element, attribute="disabled")
            if attributeValue is not None:
                enabled = element.is_enabled()
            else:
                value = self.getElementAttributeValue(element=element, attribute="class")
                self.log.info("Attribute value From Application Web UI --> :: " + value)
                enabled = not ("disabled" in value)
            if enabled:
                self.log.info("Element :: '" + info + "' is enabled")
            else:
                self.log.info("Element :: '" + info + "' is not enabled")
        except:
            self.log.error("Element :: '" + info + "' state could not be found")
        return enabled

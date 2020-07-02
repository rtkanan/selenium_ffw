from pages.base_page import BasePage
import utilities.custom_logger as logger
import logging
import random

class RegisterCoursesPage(BasePage):
    log = logger.customLogger(logging.DEBUG)

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
    
    # Locators
    _search_field = "search-courses"
    _search_button = "search-course-button"
    _course = "//div[@class='course-listing-title' and @title='<course_title>']"
    _enroll_button = "//button[contains(@id, 'enroll-button')]"
    _cc_num = "//input[@name='cardnumber']"
    _cc_exp_date = "//input[@name='exp-date']"
    _cc_cvc = "//input[@name='cvc']"
    _cc_pin = "//input[@name='postal']"
    _terms = "agreed_to_terms_checkbox"
    _enroll_pay_button = "confirm-purchase"

    # Actions
    def enterSearchContent(self, course):
        self.sendKeys(course, self._search_field)
    
    def clickSearchButton(self):
        self.clickElement(self._search_button)
    
    def clickCourse(self, course_title):
        course_title = self._course.replace('<course_title>', course_title)
        self.clickElement(course_title, "xpath")
    
    def clickEnrollButton(self):
        elements = self.getElementList(self._enroll_button, "xpath")
        element = random.choice(elements)
        self.clickElement(element=element)
    
    def enterDataInIframe(self, data, iframe_locator, elem_locator):
        self.switch_to_frame(iframe_locator)
        self.sendKeys(data, elem_locator, "xpath")
        self.switch_to_default()
    
    def clickTermsCheckbox(self):
        self.clickElement(self._terms)

    def clickEnrollSubmit(self):
        self.clickElement(self._enroll_pay_button)
    
    # Functionality
    def searchCourse(self, course):
        self.enterSearchContent(course)
        self.clickSearchButton()
    
    def selectCourse(self, course_title):
        self.clickCourse(course_title)
        self.clickEnrollButton()
    
    def enterCreditCardDetails(self, cc_no="", cc_exp_date="", cc_cvc="", cc_pin=""):
        self.scroll()        
        self.enterDataInIframe(cc_no, "__privateStripeFrame12", self._cc_num)
        self.enterDataInIframe(cc_exp_date, "__privateStripeFrame13", self._cc_exp_date)
        self.enterDataInIframe(cc_cvc, "__privateStripeFrame14", self._cc_cvc)
        self.enterDataInIframe(cc_pin, "__privateStripeFrame15", self._cc_pin)

    def enroll(self, cc_no, cc_exp_date, cc_cvc, cc_pin):
        self.enterCreditCardDetails(cc_no, cc_exp_date, cc_cvc, cc_pin)
        self.clickTermsCheckbox()
        # self.clickEnrollSubmit()
        # self.util.sleep(15)
    
    def verifyEnrollFailed(self):
        result = self.isEnabled(locator=self._enroll_pay_button, info="Enroll Pay Button")
        return not result
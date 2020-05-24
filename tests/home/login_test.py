import unittest
import pytest

from pages.home.login_page import LoginPage
from utilities.test_status import TestStatus

@pytest.mark.usefixtures("cSetup") # This applies the passed fixtures to all the methods availabled in the class
class LoginTests(unittest.TestCase):
    @pytest.fixture(autouse=True) 
    # This enables to use the variable defined in the method to be accessible in the other methods of the class.
    def classSetup(self, cSetup):
        self.lp = LoginPage(self.driver)
        self.ts = TestStatus(self.driver)

    def testInvalidLogin(self):
        self.lp.login()
        title_result = self.lp.verifyTitle("test")
        self.ts.mark(title_result, "Title Verification")

        lf_result = self.lp.verifyLoginFailure()
        self.ts.markFinal("testInvalidLogin", lf_result, "Login Failure")

    def testValidLogin(self):
        self.lp.login('test@email.com', "abcabc")
        
        gravatar = self.lp.verifyLoginSuccessful()
        assert gravatar == True
    

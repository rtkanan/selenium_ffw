import unittest
import pytest

from pages.courses.register_courses_page import RegisterCoursesPage
from utilities.test_status import TestStatus

@pytest.mark.usefixtures("cSetup") # This applies the passed fixtures to all the methods availabled in the class
class RegisterCoursesTests(unittest.TestCase):
    @pytest.fixture(autouse=True) 
    # This enables to use the variable defined in the method to be accessible in the other methods of the class.
    def classSetup(self, cSetup):
        self.rcp = RegisterCoursesPage(self.driver)
        self.ts = TestStatus(self.driver)
    
    def testInvalidEnrollment(self):
        self.rcp.searchCourse("javascript")
        self.rcp.selectCourse("JavaScript for beginners")
        self.rcp.enroll()
        
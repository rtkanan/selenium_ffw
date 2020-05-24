import pytest
from selenium import webdriver
from base.webdriver_factory import WebDriverFactory

# This decorator is used to mark the function as a fixture.
# @pytest.yield_fixture() # Works in all the versions
@pytest.fixture() # Syntax after pytest version 2.10
def setUp():
    print("Execute before each test case")
    yield 
    print("Execute after each test case")

# Define the fixture scope to each class rather than each function.
@pytest.fixture(scope="class")
def cSetup(request, browser):
    print("Execute before each class")
    wdf = WebDriverFactory(browser)
    driver = wdf.getWebDriverInstance()

    base_url = "https://letskodeit.teachable.com/"
    driver.get(base_url)
    
    if request.cls is not None:
        request.cls.driver = driver
    yield driver
    driver.quit()
    print("Execute after each module")

def pytest_addoption(parser):
    parser.addoption("--browser")
    parser.addoption("--ostype", help="Type of Operating System")

@pytest.fixture(scope="session")
def browser(request):
    return request.config.getoption("--browser")
    
@pytest.fixture(scope="session")
def ostype(request):
    return request.config.getoption("--ostype")
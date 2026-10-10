# base_page.py

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    TIMEOUT = 10

    def __init__(self, driver):
        self.driver = driver

    def open(self, url):
        self.driver.get(url)

    def find(self, by, value):
        return self.driver.find_element(by, value)

    def find_all(self, by, value):
        return self.driver.find_elements(by, value)

    def find_all_wait(self, by, value):
        WebDriverWait(self.driver, self.TIMEOUT).until(
            EC.presence_of_all_elements_located((by, value))
        )
        return self.find_all(by, value)

    def click(self, by, value):
        self.find(by, value).click()

    def type(self, by, value, text):
        self.find(by, value).send_keys(text)

    def get_text(self, by, value):
        return self.find(by, value).text

    def is_displayed(self, by, value):
        return self.find(by, value).is_displayed()

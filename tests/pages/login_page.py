from selenium.webdriver.common.by import By

from .base_page import BasePage


class LoginPage(BasePage):

    URL = "https://www.saucedemo.com"

    USERNAME = (By.ID, "user-name")
    PASSWORD = (By.ID, "password")
    LOGIN_BTN = (By.ID, "login-button")
    ERROR_CONTAINER = (By.CSS_SELECTOR, ".error-message-container.error")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "h3[data-test='error']")

    def open(self):
        self.driver.get(self.URL)

    def login(self, user, password):
        self.type(*self.USERNAME, user)
        self.type(*self.PASSWORD, password)
        self.click(*self.LOGIN_BTN)

    def get_error_container(self):
        return self.find(*self.ERROR_CONTAINER)

    def get_error_message(self):
        return self.get_text(*self.ERROR_MESSAGE)

    def is_login_button_displayed(self):
        return self.is_displayed(*self.LOGIN_BTN)

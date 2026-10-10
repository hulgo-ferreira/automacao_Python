from tests.pages.login_page import LoginPage


class LoginTransaction:
    def __init__(self, driver=None, username="standard_user", password="secret_sauce"):
        self.driver = driver
        self.username = username
        self.password = password
        self.login_page = None

    def run(self, driver=None):
        if driver is not None:
            self.driver = driver

        self.login_page = LoginPage(self.driver)
        self.login_page.open()
        self.login_page.login(self.username, self.password)
        return self.driver.current_url

    def login(self, driver=None):
        if driver is not None:
            self.driver = driver
        return self.run(self.driver)

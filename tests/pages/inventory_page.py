from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select

from .base_page import BasePage


class InventoryPage(BasePage):

    INVENTORY_CONTAINER = (By.ID, "inventory_container")
    APP_LOGO = (By.CLASS_NAME, "app_logo")
    MENU_BUTTON = (By.ID, "react-burger-menu-btn")
    MENU = (By.CSS_SELECTOR, ".bm-menu-wrap")
    MENU_ITEMS = (By.CLASS_NAME, "bm-item")

    ADD_BACKPACK = (By.ID, "add-to-cart-sauce-labs-backpack")
    CART = (By.CLASS_NAME, "shopping_cart_link")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    SORT = (By.CLASS_NAME, "product_sort_container")
    PRODUCTS = (By.CLASS_NAME, "inventory_item")
    PRODUCT_NAMES = (By.CLASS_NAME, "inventory_item_name")
    PRODUCT_PRICES = (By.CLASS_NAME, "inventory_item_price")

    def _product_button(self, product_id, action):
        return By.ID, f"{action}-to-cart-{product_id}"

    def is_loaded(self):
        return self.is_displayed(*self.INVENTORY_CONTAINER)

    def add_product(self):
        self.click(*self.ADD_BACKPACK)

    def get_app_logo_text(self):
        return self.get_text(*self.APP_LOGO)

    def menu_button_is_visible(self):
        return self.is_displayed(*self.MENU_BUTTON)

    def open_menu(self):
        self.driver.execute_script("document.getElementById('react-burger-menu-btn').click();")

    def menu_is_open(self):
        return self.driver.execute_script(
            "const menu = document.querySelector('.bm-menu-wrap'); return !!menu && menu.getAttribute('aria-hidden') === 'false';"
        )

    def add_product_by_id(self, product_id):
        self.click(*self._product_button(product_id, "add"))

    def get_product_ids_in_order(self):
        buttons = self.driver.find_elements(By.CSS_SELECTOR, "button[id^='add-to-cart-']")
        return [button.get_attribute("id").replace("add-to-cart-", "") for button in buttons]

    def first_two_product_ids(self):
        return self.get_product_ids_in_order()[:2]

    def remove_product_by_id(self, product_id):
        self.click(*self._product_button(product_id, "remove"))

    def go_to_cart(self):
        self.click(*self.CART)

    def sort_by(self, value):
        Select(self.find(*self.SORT)).select_by_value(value)

    def get_product_count(self):
        return len(self.find_all_wait(*self.PRODUCTS))

    def get_product_names(self):
        return [product.text for product in self.find_all(*self.PRODUCT_NAMES)]

    def get_product_prices(self):
        return [
            float(product.text.replace("$", ""))
            for product in self.find_all(*self.PRODUCT_PRICES)
        ]

    def get_cart_badge_count(self):
        badge_count = {"value": 0}

        def read_badge_count(driver):
            try:
                badges = driver.find_elements(*self.CART_BADGE)
                if not badges:
                    badge_count["value"] = 0
                    return True
                badge_text = badges[0].text.strip()
                if not badge_text:
                    return False
                badge_count["value"] = int(badge_text)
                return True
            except StaleElementReferenceException:
                return False

        WebDriverWait(self.driver, self.TIMEOUT).until(read_badge_count)
        return badge_count["value"]

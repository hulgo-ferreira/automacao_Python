import pytest

from tests.pages.inventory_page import InventoryPage
from tests.transactions.authentication import LoginTransaction


@pytest.mark.smoke
def test_login_saucedemo_sucesso(driver):
    LoginTransaction(driver).login()

    inventory_page = InventoryPage(driver)

    assert "inventory.html" in driver.current_url
    assert inventory_page.is_loaded()
    assert inventory_page.get_app_logo_text() == "Swag Labs"
    assert inventory_page.menu_button_is_visible()
    inventory_page.open_menu()
    assert inventory_page.menu_is_open()

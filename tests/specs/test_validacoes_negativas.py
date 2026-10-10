import pytest

from tests.pages.login_page import LoginPage
from tests.transactions.authentication import LoginTransaction
from tests.transactions.checkout import CheckoutTransaction
from tests.transactions.shopping import ShoppingTransaction


@pytest.mark.parametrize(
    "username,password,expected_message",
    [
        (
            "invalid_user",
            "invalid_password",
            "Epic sadface: Username and password do not match any user in this service",
        ),
        ("", "", "Epic sadface: Username is required"),
        (
            "locked_out_user",
            "secret_sauce",
            "Epic sadface: Sorry, this user has been locked out.",
        ),
    ],
)
def test_login_com_dados_invalidos(driver, username, password, expected_message):
    transaction = LoginTransaction(username=username, password=password)
    transaction.run(driver)

    login_page = LoginPage(driver)
    error_message = login_page.get_error_message()

    assert expected_message == error_message
    if username == "locked_out_user":
        error_container = login_page.get_error_container()
        assert "error" in error_container.get_attribute("class")


@pytest.mark.parametrize(
    "first_name,last_name,postal_code,expected_message",
    [
        ("", "", "", "First Name is required"),
        ("Gustavo", "", "", "Last Name is required"),
        ("Gustavo", "QA", "", "Postal Code is required"),
    ],
)
def test_checkout_com_campos_obrigatorios_ausentes(
    driver, first_name, last_name, postal_code, expected_message
):
    LoginTransaction().run(driver)
    shopping = ShoppingTransaction(driver)
    shopping.add_backpack()
    shopping.open_cart()
    checkout = CheckoutTransaction(driver)
    checkout.run()
    checkout.fill_form(first_name, last_name, postal_code)
    checkout.continue_without_data()

    assert expected_message in checkout.error_message()

from tests.transactions.authentication import LoginTransaction
from tests.transactions.checkout import CheckoutTransaction
from tests.transactions.shopping import ShoppingTransaction


def test_compra_com_multiplos_itens_valida_subtotal(driver):
    LoginTransaction().run(driver)
    shopping = ShoppingTransaction(driver)
    shopping.sort_products_by("lohi")

    first_two_ids = shopping.first_two_product_ids()
    shopping.add_products(first_two_ids)
    assert shopping.cart_badge_count() == 2

    shopping.open_cart()
    first_two_names = shopping.product_names()[:2]
    assert shopping.cart_item_names() == first_two_names

    expected_subtotal = sum(shopping.cart_item_prices())

    checkout = CheckoutTransaction(driver)
    checkout.run()
    checkout.fill_form("Gustavo", "QA", "12345")
    checkout.continue_checkout()

    assert checkout.subtotal() == expected_subtotal

    checkout.finish()
    assert checkout.get_success_message() == "Thank you for your order!"
    assert checkout.success_image_is_displayed()

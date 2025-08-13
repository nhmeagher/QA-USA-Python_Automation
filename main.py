import data
import helpers
from selenium import webdriver
from pages import UrbanRoutesPage

class TestUrbanRoutes:
    @classmethod
    def setup_class(cls):
        from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(5)
        if helpers.is_url_reachable(data.URBAN_ROUTES_URL):
            print("Connected to server")
        else:
            print("Unable to connect")

    # 1. Set route
    def test_set_route(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        p = UrbanRoutesPage(self.driver)
        p.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        assert p.get_from() == data.ADDRESS_FROM
        assert p.get_to() == data.ADDRESS_TO

    # 2. Select Supportive
    def test_select_plan(self):
        p = UrbanRoutesPage(self.driver)
        p.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        p.call_taxi()
        p.select_supportive()
        assert p.select_supportive() is True

    # 3. Phone Number
    def test_fill_phone_number(self):
        p = UrbanRoutesPage(self.driver)
        p.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        p.call_taxi()
        p.select_supportive()
        p.enter_phone_number(data.PHONE_NUMBER)
        assert data.PHONE_NUMBER == p.enter_phone_number()

    # 4. Add Card
    def test_fill_card(self):
        p = UrbanRoutesPage(self.driver)
        p.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        p.call_taxi()
        p.select_supportive()
        p.enter_phone_number(data.PHONE_NUMBER)
        p.add_card(data.CARD_NUMBER, data.CARD_CODE)
        assert p.get_payment_method_text() == "Card"

    # 5. Comment
    def test_comment_for_driver(self):
        p = UrbanRoutesPage(self.driver)
        p.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        p.select_supportive()
        p.set_comment(data.MESSAGE_FOR_DRIVER)
        assert p.get_comment() == data.MESSAGE_FOR_DRIVER

    # 6. Blanket & Handkerchiefs
    def test_order_blanket_and_handkerchiefs(self):
        p = UrbanRoutesPage(self.driver)
        p.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        p.call_taxi()
        p.select_supportive()
        assert p.set_blanket_and_handkerchiefs(True) is True

    # 7. Two ice creams
    def test_order_2_ice_creams(self):
        p = UrbanRoutesPage(self.driver)
        p.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        p.call_taxi()
        p.select_supportive()
        count = p.add_ice_creams(2)
        assert count == 2

    # 8. Order → car search modal
    def test_car_search_model_appears(self):
        p = UrbanRoutesPage(self.driver)
        p.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        p.call_taxi()
        p.select_supportive()
        p.enter_phone_number(data.PHONE_NUMBER)
        p.set_comment(data.MESSAGE_FOR_DRIVER)
        p.order()
        assert p.is_car_search_modal_visible() is True

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
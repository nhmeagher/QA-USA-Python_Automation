import data
import helpers


class TestUrbanRoutes:
    @classmethod
    def setup_class(cls):
        if helpers.is_url_reachable(data.URBAN_ROUTES_URL):
            print("Connected to the Urban Routes server")
        else:
            print("Cannot connect to the Urban Routes. Check the server is on and still running")


def test_set_route(self):  # Add in S8
    print("function created for set route")
    pass


def test_select_plan(self):
    # Add in S8
    print("function created for test_select_plan")
    pass


def test_fill_phone_number(self):
    # Add in S8
    print("function created for test_fill_phone_number")
    pass


def test_fill_card(self):
    # Add in S8
    print("function created for test_fill_card")
    pass


def test_comment_for_driver(self):
    # Add in S8
    print("function created for test_comment_for_driver")
    pass


def test_order_blanket_and_handkerchiefs(self):
    # Add in S8
    print("function created for test_order_blanket_and_handkerchiefs")
    pass


def test_order_2_ice_creams(self):
    for i in range(2):  # This loops 2 times
        # Add in S8
        print("function created for test_order_2_ice_creams")
    pass


def test_car_search_model_appears(self):
    # Add in S8
    print("function created for test_car_search_model_appears")
    pass

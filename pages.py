import time
from selenium import webdriver
from selenium.webdriver.common.by import By

import data
from helpers import retrieve_phone_code

# Initialize a new instance of the Chrome WebDriver
driver = webdriver.Chrome()

# Open the specified URL in the browser
driver.get(data.URBAN_ROUTES_URL)

# Pause execution for 2 seconds to allow the page to load fully
time.sleep(2)


class UrbanRoutesPage:
    # Locators
    FROM_FIELD = (By.CSS_SELECTOR, "input#from")
    TO_FIELD = (By.CSS_SELECTOR, "input#to")
    CALL_TAXI_BTN = (By.CSS_SELECTOR, "button[data-testid='call_taxi']")

    SUPPORTIVE_TARIFF_CARD = (By.XPATH, "//div[@class='tcard-title' and normalize-space()='Supportive']")

    # Phone
    PHONE_NUMBER_INPUT = (By.CSS_SELECTOR, "input#phone")
    PHONE_MODAL_REQUEST_BTN = (By.XPATH, "(//div[contains(@class,'np-button')][.//div[contains(@class,'np-text') and normalize-space()='Phone number']])[1]")
    PHONE_NEXT_BTN = (By.XPATH, "//button[@type='submit' and normalize-space()='Next']")

    # SMS CODE
    SMS_CODE = (By.CSS_SELECTOR, "input#code.card-input")
    SMS_CODE_SUBMIT_BTN = (By.XPATH, "//button[contains(@class,'button') and contains(@class,'full') and normalize-space()='Confirm']")

    # Payment
    PAYMENT_METHOD = (By.XPATH, "//div[@class='pp-text' and normalize-space()='Payment method']")
    ADD_CARD_BTN = (By.XPATH, "//img[contains(@class,'pp-plus')]")
    CARD_NUMBER_INPUT = (By.CSS_SELECTOR, "input#number.card-input")
    CARD_CVV_INPUT = (By.XPATH, "//input[@id='code' and contains(@class,'card-input')]")
    LINK_CARD_BTN = (By.CSS_SELECTOR, "button[type='submit'].button.full")
    CLOSE_LINK_CARD = (By.XPATH, "//*[@id='root']/div/div[contains(@class,'payment-picker')]/div[contains(@class,'modal')]/div[contains(@class,'section') and contains(@class,'active')]/button")

    # Comment
    COMMENT_INPUT = (By.CSS_SELECTOR, "input[name='comment']")

    # Blanket & Handkerchiefs
    BLANKET_HANDKERCHIEF_TOGGLE_CLICK = (
        By.XPATH,
        "//*[contains(.,'Blanket') and contains(.,'handkerchief')]/ancestor::*[self::label or self::div][1]"
        "//*[@role='switch' or self::span or self::div][last()]"
    )
    # Read actual state from the checkbox (not the slider)
    BLANKET_HANDKERCHIEF_TOGGLE_STATE = (
        By.XPATH,
        "//div[@class='r-sw-label' and normalize-space()='Blanket and handkerchiefs']"
        "/following-sibling::div[@class='r-sw'][1]//input[@type='checkbox']"
    )

    # Ice cream
    ICECREAM_ADD_BTN = (By.XPATH, "//*[contains(.,'Ice cream')]/ancestor::*[self::div or self::section][1]//div[contains(@class,'counter-plus')]")
    ICECREAM_COUNT = (By.XPATH, "//*[contains(.,'Ice cream')]/ancestor::*[self::div or self::section][1]//div[contains(@class,'counter-value')]")

    # Order (click the button that wraps the span)
    ORDER_BTN = (By.XPATH, "//span[@class='smart-button-main' and normalize-space()='Enter the number and order']/ancestor::button[1]")
    CAR_SEARCH_MODAL = (By.XPATH, "//div[@class='order-body']")

    # Initialize driver
    def __init__(self, driver):
        self.driver = driver

    # Input Addresses
    def enter_from_location(self, from_text):
        self.driver.find_element(*self.FROM_FIELD).send_keys(from_text)

    def enter_to_location(self, to_text):
        self.driver.find_element(*self.TO_FIELD).send_keys(to_text)

    # Call taxi
    def call_taxi(self):
        self.driver.find_element(*self.CALL_TAXI_BTN).click()

    # Supportive Tariff
    def select_supportive(self):
        self.driver.find_element(*self.SUPPORTIVE_TARIFF_CARD).click()

    # Phone number
    def phone_number_modal(self):
        self.driver.find_element(*self.PHONE_MODAL_REQUEST_BTN).click()
        time.sleep(0.5)

    def enter_phone_number(self, phone_number):
        self.driver.find_element(*self.PHONE_NUMBER_INPUT).send_keys(phone_number)
        time.sleep(0.5)

    def click_phone_next(self):
        self.driver.find_element(*self.PHONE_NEXT_BTN).click()
        time.sleep(0.5)

    # SMS code
    def enter_sms_code(self, _sms_code_ignored=None):
        # Retrieve the SMS code from logs
        code = retrieve_phone_code(self.driver)
        # Enter code and submit
        self.driver.find_element(*self.SMS_CODE).send_keys(code)
        self.driver.find_element(*self.SMS_CODE_SUBMIT_BTN).click()
        time.sleep(1)

    # Payment card flow
    def add_card(self, number, cvv):
        self.driver.find_element(*self.PAYMENT_METHOD).click()
        time.sleep(0.5)
        self.driver.find_element(*self.ADD_CARD_BTN).click()
        time.sleep(0.5)
        self.driver.find_element(*self.CARD_NUMBER_INPUT).send_keys(number)
        self.driver.find_element(*self.CARD_CVV_INPUT).send_keys(cvv)
        self.driver.find_element(*self.LINK_CARD_BTN).click()
        time.sleep(1)
        self.driver.find_element(*self.CLOSE_LINK_CARD).click()
        time.sleep(0.5)

    # Comment for driver
    def set_comment(self, text):
        el = self.driver.find_element(*self.COMMENT_INPUT)
        el.clear()
        el.send_keys(text)
        time.sleep(0.3)

    # Blanket & Handkerchiefs toggle
    def set_blanket_and_handkerchiefs(self, enable=True):
        state_el = self.driver.find_element(*self.BLANKET_HANDKERCHIEF_TOGGLE_STATE)
        current = bool(state_el.get_attribute("checked")) or bool(state_el.is_selected())
        if current != enable:
            self.driver.find_element(*self.BLANKET_HANDKERCHIEF_TOGGLE_CLICK).click()
            time.sleep(0.5)
        # Return updated state
        state_el = self.driver.find_element(*self.BLANKET_HANDKERCHIEF_TOGGLE_STATE)
        return bool(state_el.get_attribute("checked")) or bool(state_el.is_selected())

    # Ice creams
    def add_ice_creams(self, n):
        btn = self.driver.find_element(*self.ICECREAM_ADD_BTN)
        for _ in range(n):
            btn.click()
            time.sleep(0.1)
        txt = self.driver.find_element(*self.ICECREAM_COUNT).text.strip()
        digits = "".join(ch for ch in txt if ch.isdigit())
        return int(digits or "0")

    # Final order
    def order(self):
        self.driver.find_element(*self.ORDER_BTN).click()
        time.sleep(1)

    # Car modal visible
    def is_car_search_modal_visible(self):
        self.driver.find_element(*self.CAR_SEARCH_MODAL)



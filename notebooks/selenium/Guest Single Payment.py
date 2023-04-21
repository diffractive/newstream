# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.11.4
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# +
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

from diffractive.selenium import wait_element, ScreenGrabber, get_webdriver, notebook_root
from diffractive.selenium.visualisation import gallery

from components import Application

import secrets
import time

# +
randstr = secrets.token_hex(6).upper()

email = f'test_user{randstr}@newstream.com'
name = 'Test User'
card_number = '4242424242424242'
card_expiry = '1133'
cvc = '123'
# -

driver = get_webdriver('portal')
grabber = ScreenGrabber(driver)
app = Application(driver)

app.go()
grabber.capture_screen('home_page', 'Home')

app.link('Donation Form').click()
grabber.capture_screen('donation_form', 'Donation Form')

# Cannot go to the signup page without setting a value into the custom amount or choosing a default from selector
app.dropdown('id_donation_amount').select(1)
app.input('id_email').fill(email)
app.input('id_name').fill(name)
app.dropdown('id_payment_gateway').select(1)
app.button('Continue as guest').click()
grabber.capture_screen('guest_payment', 'Confirm Payment')

app.button('Confirm Donation').click()
grabber.capture_screen('processing_payment', 'Processing Payment')

# Wait until redirecting finishes
time.sleep(15)
grabber.capture_screen('stripe_payment_gateway', 'Stripe payment gateway')

app.input('cardNumber').fill(card_number)
app.input('cardExpiry').fill(card_expiry)
app.input('cardCvc').fill(cvc)
app.input('billingName').fill(name)
app.button('Pay').click()
wait_element(driver, '//h1[text()="Thank you!"]')
grabber.capture_screen('thank_you', 'Thank you screen')

gallery(zip(grabber.screens.values(), grabber.captions.values()), row_height="300px")

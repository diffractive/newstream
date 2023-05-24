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

# +
randstr = secrets.token_hex(6).upper()

cancel_url = '/en/donations/cancel-from-stripe/'
email = f'test_user{randstr}@newstream.com'
first_name = 'Test'
last_name = 'User'
password = 'strongpwd'
name = 'Test User'
# -

driver = get_webdriver('portal')
grabber = ScreenGrabber(driver)
app = Application(driver)

app.go()
grabber.capture_screen('home_page', 'Home')

app.link('Donation Form').click()
grabber.capture_screen('donation_form', 'Donation Form')

# +
# Cannot go to the signup page without setting a value into the custom amount or choosing a default from selector
app.dropdown('id_donation_amount').select('HKD $100')
app.dropdown('id_donation_frequency').select('Monthly')
app.dropdown('id_payment_gateway').select('Stripe')

# We need to first sign up with an account in order to use a user payment
app.button('Register or Login').click()
grabber.capture_screen('sign_in_sign_up', 'Sign in or Sign up page')
# -

app.link('Continue with Email Sign up').click()
grabber.capture_screen('sign_up', 'Sign up form')

app.input('id_email').fill(email)
app.input('id_first_name').fill(first_name)
app.input('id_last_name').fill(last_name)
app.input('id_password1').fill(password)
app.input('id_password2').fill(password)
grabber.capture_screen('filled_form', 'Filled signup form')

app.button('Continue').click()
grabber.capture_screen('signed_up', 'Successfully signed up')

app.button('Confirm Donation').click()
grabber.capture_screen('processing_payment', 'Processing Payment')

# Wait until redirecting finishes
wait_element(driver, '//input[@id="cardNumber"]')
grabber.capture_screen('stripe_payment_gateway', 'Stripe payment gateway')

app.link(cancel_url).click()
wait_element(driver, '//h1[text()="Donation Cancelled"]')
grabber.capture_screen('cancelled', 'Cancelled Donation')

gallery(zip(grabber.screens.values(), grabber.captions.values()), row_height="300px")


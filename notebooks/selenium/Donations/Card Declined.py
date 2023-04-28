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
from utils import get_email_count, wait_for_email, get_emails

import secrets

# +
randstr = secrets.token_hex(6).upper()

email = f'test_user{randstr}@newstream.com'
name = 'Test User'
card_number = '4242424242424242'
declined_card = '4000000000000002'
card_expiry = '1133'
cvc = '123'
email_count = get_email_count()
# -

driver = get_webdriver('portal')
grabber = ScreenGrabber(driver)
app = Application(driver)

app.go()
grabber.capture_screen('home_page', 'Home')

app.link('Donation Form').click()
grabber.capture_screen('donation_form', 'Donation Form')

# Cannot go to the signup page without setting a value into the custom amount or choosing a default from selector
app.dropdown('id_donation_amount').select('USD $100')
app.input('id_email').fill(email)
app.input('id_name').fill(name)
app.dropdown('id_payment_gateway').select('Stripe')
app.button('Continue as guest').click()
grabber.capture_screen('guest_payment', 'Confirm Payment')

app.button('Confirm Donation').click()
grabber.capture_screen('processing_payment', 'Processing Payment')

# Wait until redirecting finishes
wait_element(driver, '//input[@id="cardNumber"]')
grabber.capture_screen('stripe_payment_gateway', 'Stripe payment gateway')

# ## Test card declined

app.input('cardNumber').fill(declined_card)
app.input('cardExpiry').fill(card_expiry)
app.input('cardCvc').fill(cvc)
app.input('billingName').fill(name)
app.button('Pay').click()
wait_element(driver, '//div[text()="Your credit card was declined. Try paying with a debit card instead."]')
grabber.capture_screen('declined_card', 'Card has been declined error')

# ## Happy path

app.input('cardNumber').fill(card_number)
app.input('cardExpiry').fill(card_expiry)
app.input('cardCvc').fill(cvc)
app.input('billingName').fill(name)
app.button('Pay').click()
wait_element(driver, '//h1[text()="Thank you!"]')
grabber.capture_screen('thank_you', 'Thank you screen')

# +
# There should be two emails sent, one for admins one for the user
wait_for_email(email_count+1)
emails = get_emails(0, 2)
user_email = 'Thank you for your Donation'
admin_email = 'New One-off Donation'

# Email order is not guaranteed
email_titles = [admin_email, user_email]
for email_content in emails:
    email_title = email_content['Content']['Headers']['Subject'][0]
    email_recipient = email_content['Content']['Headers']['To'][0]
    
    assert email_title in email_titles, f'Unexpected e-mail found: {email_title}'
    if email_title == user_email:
        assert email_recipient == email, \
            f"Unexpected e-mail recipient {email_recipient}, expected: {email}"
    email_titles.remove(email_title)
# -

gallery(zip(grabber.screens.values(), grabber.captions.values()), row_height="300px")



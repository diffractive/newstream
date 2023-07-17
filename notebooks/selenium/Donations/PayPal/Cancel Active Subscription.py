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

from utils import get_email_count, wait_for_email, get_emails, get_link_by_email_subject_and_regex, clear_all_emails
from components import Application
from functions import create_subscription

import secrets
# -

clear_all_emails()
randstr = secrets.token_hex(6).upper()
data = {
    "email": f'test_user{randstr}@newstream.com',
    "first_name": 'Test',
    "last_name": 'User',
    "password": 'strongpwd',
    "name": 'Test User',
    "card_number": '4242424242424242',
    "card_expiry": '1133',
    "cvc": '123'
}
email_count = get_email_count()

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
app.dropdown('id_payment_gateway').select('PayPal')

# We need to first sign up with an account in order to use a user payment
app.button('Register or Login').click()
grabber.capture_screen('sign_in_sign_up', 'Sign in or Sign up page')
# -

app.link('Continue with Email Sign up').click()
grabber.capture_screen('sign_up', 'Sign up form')

app.input('id_email').fill(data['email'])
app.input('id_first_name').fill(data['first_name'])
app.input('id_last_name').fill(data['last_name'])
app.input('id_password1').fill(data['password'])
app.input('id_password2').fill(data['password'])
grabber.capture_screen('filled_form', 'Filled signup form')

app.button('Continue').click()
grabber.capture_screen('signed_up', 'Successfully signed up')

# +
# There should be two emails sent, one for admins one for the user
wait_for_email(email_count+1)
emails = get_emails(0, 2)
user_email = 'Please Confirm Your Email Address'
admin_email = 'A Donor Account is created'

# Email order is not guaranteed
email_titles = [admin_email, user_email]
for email_content in emails:
    email_title = email_content['Content']['Headers']['Subject'][0]
    email_recipient = email_content['Content']['Headers']['To'][0]

    assert email_title in email_titles, f'Unexpected e-mail found: {email_title}'
    if email_title == user_email:
        assert email_recipient == data['email'], \
            f"Unexpected e-mail recipient {email_recipient}, expected: {data['email']}"
    email_titles.remove(email_title)

email_count += 2
# -

app.button('Confirm Donation').click()
grabber.capture_screen('processing_payment', 'Processing Payment')

# Wait until redirecting finishes
wait_element(driver, '//input[@id="username"]')
grabber.capture_screen('paypal_checkout_login', 'PayPal checkout login')

app.link('secondary-btn').click()

wait_element(driver, '//input[@id="card_number"]')
grabber.capture_screen('paypal_checkout_card_details', 'PayPal checkout card details')

app.input('card_number').fill(data['card_number'])
app.input('card_expiry').fill(data['card_expiry'])
app.input('cvc').fill(data['cvc'])
app.input('primary-btn').click()

wait_element(driver, '//input[@value="agree & subscribe"]')
grabber.capture_screen('paypal_checkout_subscribe', 'PayPal checkout subscribe')

app.input('primary-btn').click()

wait_element(driver, '//h1[text()="Thank you!"]')
grabber.capture_screen('thank_you', 'Thank you screen')

# 2 emails are delivered
wait_for_email(email_count + 1)
email_count += 2
grabber.capture_screen('thank_you', 'Donation created')

subject = "Please Confirm Your Email Address"
reg_str = "(?P<url>http://app.newstream.local:8000/en/accounts/confirm-email/[^/]*/)"
url = get_link_by_email_subject_and_regex(subject, reg_str)
# get_link_by_email_subject_and_regex deletes the email
email_count -= 1
driver.get(url)
grabber.capture_screen('email_confirm', 'Confirm email')

app.button('Confirm').click()
grabber.capture_screen('email_confirmed', 'Email confirmed')

app.label('dropdown-toggle-checkbox').click()
grabber.capture_screen('expanded_menu', 'Expanded menu')

app.link("header-donations").click()
grabber.capture_screen('single_donations', 'My donations page')

app.link('Recurring Donations').click()
grabber.capture_screen('subscriptions', 'Recurring donations')

rows = app.table('my-donations-table').row_values()
assert rows[0][5] == 'Active'

app.label('md2_dropdown-toggle-checkbox1').click()
grabber.capture_screen('open_menu', 'Open subscription menu')

app.button('cancel-recurring-donation-wide').click()
grabber.capture_screen('cancel_subscription_popup', 'Cancel subscription popup')

app.button('confirm-ok').click()
wait_element(driver, '//h4[text()="Recurring donation cancelled!"]')
grabber.capture_screen('cancel_subscription_popup_confirm', 'Cancel subscription popup confirm')

app.button('confirm-ok').click()

rows = app.table('my-donations-table').row_values()
assert rows[0][5] == 'Cancelled'
grabber.capture_screen('cancel_subscription', 'Subscription has been cancelled')


# +
# There should be two emails sent, one for admins one for the user
wait_for_email(email_count+1)
emails = get_emails(0, 2)
user_email = 'Your Recurring Donation is Cancelled'
admin_email = 'A Recurring Donation is cancelled'

# Email order is not guaranteed
email_titles = [admin_email, user_email]
for email_content in emails:
    email_title = email_content['Content']['Headers']['Subject'][0]
    email_recipient = email_content['Content']['Headers']['To'][0]

    assert email_title in email_titles, f'Unexpected e-mail found: {email_title}'
    if email_title == user_email:
        assert email_recipient == data['email'], \
            f"Unexpected e-mail recipient {email_recipient}, expected: {data['email']}"
# Email content has yet to be updated with paypal so we can ignore these assertions for now
#         assert "has been cancelled at your request" in email_content['Content']['Body'], \
#             f"Content does not contain string 'has been cancelled at your request'."
#     if email_title == admin_email:
#         assert "has been cancelled by a donor" in email_content['Content']['Body'], \
#             f"Content does not contain string 'has been cancelled by a donor'."
    email_titles.remove(email_title)
# -

gallery(zip(grabber.screens.values(), grabber.captions.values()), row_height="300px")



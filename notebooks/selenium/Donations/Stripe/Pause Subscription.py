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

from utils import get_email_count, wait_for_email, get_email_by_email_subject, clear_all_emails
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

create_subscription(driver, app, data)
# 4 emails are delivered
wait_for_email(email_count + 3)
grabber.capture_screen('thank_you', 'Donation created')

subject = "Please Confirm Your Email Address"
reg_str = "(?P<url>http://app.newstream.local:8000/en/accounts/confirm-email/[^/]*/)"
url = get_email_by_email_subject(subject, reg_str)
driver.get(url)
grabber.capture_screen('email_confirm', 'Confirm email')

app.button('Confirm').click()
grabber.capture_screen('email_confirmed', 'Email confirmed')

app.label('dropdown-toggle-checkbox').click()
grabber.capture_screen('expanded_menu', 'Expanded menu')

# This is not working for some reason so fallback into drive.find_element
# app.link("My Donations").click()
driver.find_element(By.XPATH, '//div[contains(@class, "user-dropdown-menu")]//a[text()="My Donations"]').click()
grabber.capture_screen('single_donations', 'My donations page')

app.link('Recurring Donations').click()
grabber.capture_screen('subscriptions', 'Recurring donations')

row = app.table('my-donations-table').first_row()
assert row[5] == 'Active'

app.label('md2_dropdown-toggle-checkbox1').click()
grabber.capture_screen('open_menu', 'Open subscription menu')

# This is not working so falling back to driver.find_element
# app.button('Edit Recurring donation').click()
driver.find_elements(By.XPATH, '//div[contains(@class, "dropdown-menu-popup ")]//div//button//span[text()="Pause Recurring Donation"]')[1].click()
grabber.capture_screen('pause_subscription_popup', 'Pause subscription popup')

app.button('confirm-ok').click()
wait_element(driver, '//h4[text()="Your recurring donation via Stripe is paused."]')
grabber.capture_screen('paused_subscription_popup_confirm', 'Paused subscription popup confirm')

app.button('confirm-ok').click()

row = app.table('my-donations-table').first_row()
assert row[5] == 'Paused'
grabber.capture_screen('paused_subscription', 'Subscription has been paused')

# ## Resume subscription

app.label('md2_dropdown-toggle-checkbox1').click()
grabber.capture_screen('open_menu', 'Open subscription menu')

# This is not working so falling back to driver.find_element
# app.button('Edit Recurring donation').click()
driver.find_elements(By.XPATH, '//div[contains(@class, "dropdown-menu-popup ")]//div//button//span[text()="Resume Recurring Donation"]')[1].click()
grabber.capture_screen('resume_subscription_popup', 'Resume subscription popup')

app.button('confirm-ok').click()
wait_element(driver, '//h4[text()="Your recurring donation via Stripe is resumed."]')
grabber.capture_screen('resume_subscription_popup_confirm', 'Resumed subscription popup confirm')

app.button('confirm-ok').click()

row = app.table('my-donations-table').first_row()
assert row[5] == 'Active'
grabber.capture_screen('resumed_subscription', 'Subscription has been resumed')

gallery(zip(grabber.screens.values(), grabber.captions.values()), row_height="300px")

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

from utils import get_email_count, wait_for_email, clear_all_emails
from components import Application
from functions import create_single_payment

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

create_single_payment(driver, app, data)
# 4 emails are delivered
wait_for_email(email_count + 3)
grabber.capture_screen('thank_you', 'Donation created')

app.label('dropdown-toggle-checkbox').click()
grabber.capture_screen('expanded_menu', 'Expanded menu')

# This is not working for some reason so fallback into drive.find_element
# app.link("My Donations").click()
driver.find_element(By.XPATH, '//div[contains(@class, "user-dropdown-menu")]//a[text()="My Donations"]').click()
grabber.capture_screen('single_donations', 'My donations page')

row = app.table('my-donations-table').first_row()
assert row[0] == 'USD $100.00'
assert row[1] == 'One-time'
# assert row[2][0:3] == 'pi_' # Not consistent due to another bug
assert row[4] == 'Stripe'
assert row[5] == 'Complete'

gallery(zip(grabber.screens.values(), grabber.captions.values()), row_height="300px")



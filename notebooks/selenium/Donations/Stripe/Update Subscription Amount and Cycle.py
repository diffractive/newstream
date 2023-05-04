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

from utils import get_email_count, wait_for_email, get_email_by_email_subject
from components import Application
from functions import create_subscription

import secrets
# -

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
new_amount = '50'
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
assert row[0] == 'USD $100.00'


app.label('md2_dropdown-toggle-checkbox1').click()
grabber.capture_screen('open_menu', 'Open subscription menu')

# This is not working so falling back to driver.find_element
# app.button('Edit Recurring donation').click()
driver.find_elements(By.XPATH, '//div[contains(@class, "dropdown-menu-popup ")]//div//button[text()="Edit Recurring donation"]')[1].click()
grabber.capture_screen('edit_subscription', 'Edit subscription page')

app.input('id_recurring_amount').clear()
app.input('id_recurring_amount').fill(new_amount)
app.label('Change Billing Cycle to Now').click()
grabber.capture_screen('updated_values', 'Updated values')

app.button('Update Recurring Donation').click()
grabber.capture_screen('update_cycle', 'Update cycle')

# Messages block the button so go directly to subscriptions
app.go('en/donations/my-recurring-donations/')
grabber.capture_screen('updated_amount_list', 'Update amount list')


app.label('md2_dropdown-toggle-checkbox1').click()
driver.find_elements(By.XPATH, '//div[contains(@class, "dropdown-menu-popup ")]//div//button[text()="View all renewals"]')[1].click()
grabber.capture_screen('all_renewals', 'All renewals')

row = app.table('my-donations-table').first_row()
assert row[0] == f'USD ${new_amount}.00'

gallery(zip(grabber.screens.values(), grabber.captions.values()), row_height="300px")



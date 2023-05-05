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

from utils import get_email_count, wait_for_email, get_email_by_email_subject, clear_all_emails, get_emails
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
email_count += 4
grabber.capture_screen('thank_you', 'Donation created')

subject = "Please Confirm Your Email Address"
reg_str = "(?P<url>http://app.newstream.local:8000/en/accounts/confirm-email/[^/]*/)"
url = get_email_by_email_subject(subject, reg_str)
# get_email_by_email_subject deletes the email
email_count -= 1
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


app.label('md2_dropdown-toggle-checkbox1').click()
grabber.capture_screen('open_menu', 'Open subscription menu')

# This is not working so falling back to driver.find_element
# app.button('Edit Recurring donation').click()
driver.find_elements(By.XPATH, '//div[contains(@class, "dropdown-menu-popup ")]//div//button[text()="Edit Recurring donation"]')[1].click()
grabber.capture_screen('edit_subscription', 'Edit subscription page')

app.label('Change Billing Cycle to Now').click()
app.button('Update Recurring Donation').click()
grabber.capture_screen('update_cycle', 'Update cycle')

app.link('Back to My Donations').click()
grabber.capture_screen('updated_amount_list', 'Update amount list')


app.label('md2_dropdown-toggle-checkbox1').click()
driver.find_elements(By.XPATH, '//div[contains(@class, "dropdown-menu-popup ")]//div//button[text()="View all renewals"]')[1].click()
grabber.capture_screen('all_renewals', 'All renewals')

# +
# There should be two emails sent, one for admins one for the user
wait_for_email(email_count+1)
emails = get_emails(0, 2)
user_email = 'Your Recurring Donation is Rescheduled'
admin_email = 'A Recurring Donation is Rescheduled'

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
# -

gallery(zip(grabber.screens.values(), grabber.captions.values()), row_height="300px")



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

create_subscription(driver, app, data)
# 4 emails are delivered
wait_for_email(email_count + 3)
email_count += 4
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
        assert "has been cancelled at your request" in email_content['Content']['Body'], \
            f"Content does not contain string 'has been cancelled at your request'."
    if email_title == admin_email:
        assert "has been cancelled by a donor" in email_content['Content']['Body'], \
            f"Content does not contain string 'has been cancelled by a donor'."
    email_titles.remove(email_title)
# -

gallery(zip(grabber.screens.values(), grabber.captions.values()), row_height="300px")



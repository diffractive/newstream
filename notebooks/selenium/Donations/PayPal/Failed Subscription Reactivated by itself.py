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
from functions import create_paypal_subscription
from paypal_api import PayPal

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
paypal = PayPal()

create_paypal_subscription(driver, app, data)
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

# Get subscription id and advance subscription to next successful payment cycle
app.go('en/donations/my-recurring-donations/')
rows = app.table('my-donations-table').row_values()
sub_id = rows[0][2]
paypal.simulate_next_payment_cycle(sub_id, "success")

# Check renewal records
app.label('md2_dropdown-toggle-checkbox1').click()
grabber.capture_screen('open_menu', 'Open subscription menu')

rows = app.table('my-donations-table').rows()
# We need this data_id to fetch the right buttons
data_id = rows[0][5].get_attribute('data-id')
app.button('view-recurring-donation-wide', data_id).click()
grabber.capture_screen('view_renewals', 'Renewals page')

# advance subscription to next failing payment cycle
paypal.simulate_next_payment_cycle(sub_id, "failure")

# +
# There should be two emails sent, one for admins one for the user
wait_for_email(email_count+1)
emails = get_emails(0, 2)
user_email = 'Your Monthly Payment was Unsuccessful'
admin_email = 'A Recurring Donation has failed'


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

app.go('en/donations/my-recurring-donations/')
rows = app.table('my-donations-table').row_values()
assert rows[0][5] == 'Payment failed'
grabber.capture_screen('payment_failed', 'Failed payment subscriptions')

paypal.simulate_next_payment_cycle(sub_id, "success")
app.go('en/donations/my-recurring-donations/')
rows = app.table('my-donations-table').row_values()
assert rows[0][5] == 'Active'
grabber.capture_screen('successful_payment', 'Subscription is now successful again')

# +
# There should be two emails sent, one for admins one for the user
wait_for_email(email_count+1)
emails = get_emails(0, 2)
user_email = 'Your Monthly Payment is Active again'
admin_email = 'A Recurring Donation has been reactivated'


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

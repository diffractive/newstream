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

from utils import get_email_count, wait_for_email, get_link_by_email_subject_and_regex, clear_all_emails, get_emails
from components import Application
from functions import create_subscription

import secrets
import time
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
new_amount = '50'
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
assert rows[0][0] == 'USD $100.00'


app.label('md2_dropdown-toggle-checkbox1').click()
grabber.capture_screen('open_menu', 'Open subscription menu')

app.button('edit-recurring-donation-wide').click()
grabber.capture_screen('edit_subscription', 'Edit subscription page')

app.input('id_recurring_amount').clear()
app.input('id_recurring_amount').fill(new_amount)
app.label('Change Billing Cycle to Now').click()
grabber.capture_screen('updated_values', 'Updated values')

app.button('Update Recurring Donation').click()
grabber.capture_screen('update_cycle', 'Update cycle')

# +
# There should be four emails sent, two for admins two for the user
wait_for_email(email_count+3)
emails = get_emails(0, 4)
user_email_1 = 'Your Recurring Donation Amount is Adjusted'
admin_email_1 = 'A Recurring Donation Amount is Adjusted'
user_email_2 = 'Your Recurring Donation is Rescheduled'
admin_email_2 = 'A Recurring Donation is Rescheduled'

# Email order is not guaranteed
email_titles = [admin_email_1, admin_email_2, user_email_1, user_email_2]
for email_content in emails:
    email_title = email_content['Content']['Headers']['Subject'][0]
    email_recipient = email_content['Content']['Headers']['To'][0]

    assert email_title in email_titles, f'Unexpected e-mail found: {email_title}'
    if email_title == user_email_1:
        assert email_recipient == data['email'], \
            f"Unexpected e-mail recipient {email_recipient}, expected: {data['email']}"
    if email_title == user_email_2:
        assert email_recipient == data['email'], \
            f"Unexpected e-mail recipient {email_recipient}, expected: {data['email']}"
    email_titles.remove(email_title)
# -

# Wait for popups to go down
WebDriverWait(driver, 10).until(
    EC.invisibility_of_element((By.XPATH, '//p[text()="Your recurring donation amount at Stripe is updated successfully."]'))
)
app.link('Back to My Donations').click()
grabber.capture_screen('recurrent_donations', 'Recurrent Donations')


app.label('md2_dropdown-toggle-checkbox1').click()
app.button('view-recurring-donation-wide').click()
grabber.capture_screen('all_renewals', 'All renewals')

rows = app.table('my-donations-table').row_values()
assert rows[0][0] == f'USD ${new_amount}.00'

gallery(zip(grabber.screens.values(), grabber.captions.values()), row_height="300px")



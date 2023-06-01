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
import time
from stripe_api import Stripe
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
stripe = Stripe()

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
# Get subscription id and update payment method so that the payment fails
sub_id = rows[0][2]
stripe.update_to_failing_card(sub_id)
invoice_response = stripe.new_invoice_on_subscription(sub_id)
inv_id = invoice_response["id"]

# retry the max retry number for failed payments
# depends on the number configured on localstripe via the env variable MAX_PAYMENT_FAILURE_RETRIES
# if no env variable is provided, default is 3 times
for i in range(3):
    inv = stripe.retry_open_invoice(inv_id)
    # give time for webhooks events to arrive before the customer.subscription.deleted webhook
    time.sleep(1)

# wait for some more time for customer.subscription.deleted to have arrived
time.sleep(2)
app.go(url="donations/my-recurring-donations/")

rows = app.table('my-donations-table').row_values()
assert rows[0][5] == 'Cancelled'
grabber.capture_screen('cancelled_subscription', 'Subscription has been cancelled')

# +
# There should be at least 8 emails sent (6 for the 1st payment failure and the 2 retries following, and 2 for the subscription cancelled)
# Because the last pair of payment failed emails might not be seen if customer.subscription.deleted arrived first
wait_for_email(email_count+7)
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
        assert "has been cancelled due to repeated failed payments" in email_content['Content']['Body'], \
            f"Content does not contain string 'has been cancelled due to repeated failed payments'."
    if email_title == admin_email:
        assert "has been cancelled due to repeated failed payments" in email_content['Content']['Body'], \
            f"Content does not contain string 'has been cancelled due to repeated failed payments'."
    email_titles.remove(email_title)
# -

gallery(zip(grabber.screens.values(), grabber.captions.values()), row_height="300px")



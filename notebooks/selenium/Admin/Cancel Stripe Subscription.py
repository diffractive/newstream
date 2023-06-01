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
admin = {
    "email": "newstream@test.local",
    "password": "newstream"
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

# logout test user
app.label('dropdown-toggle-checkbox').click()
grabber.capture_screen('user_menu_expanded', 'Expanded user menu')

app.link("header-logout").click()
grabber.capture_screen('logged_out', 'Logged out')

# login into backend
app.go(url="admin")
app.input('id_username').fill(admin["email"])
app.input('id_password').fill(admin["password"])
grabber.capture_screen('filled_login_form', 'Filled Login Form')

app.button('button button-longrunning').click()
grabber.capture_screen('logged_in', 'Logged in')

# go to the first subscriptions detail page
app.go(url="admin/donations/subscriptioninstance/")
top_sub = driver.find_element(By.XPATH, f'//table[contains(@class, "listing")]/tbody/tr')
sub_id = top_sub.get_attribute('data-object-pk')
app.go(url="admin/donations/subscriptioninstance/inspect/%s/" % sub_id)
grabber.capture_screen('subscription_details', 'Subscription Details page')

# go to actions tab
app.link("#tab-actions").click()
WebDriverWait(driver, 10).until(
    EC.visibility_of(app.input("admin-cancel-sub").element)
)
grabber.capture_screen('actions_tab', 'Actions Tab')

# cancel the subscription
app.input("admin-cancel-sub").click()
# Wait for popup to be visible
WebDriverWait(driver, 10).until(
    EC.visibility_of(driver.find_element(By.XPATH, "//li[text()[contains(.,'Subscription %s status is cancelled.')]]" % sub_id))
)
grabber.capture_screen('subscription_cancelled', 'Subscription Cancelled')

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
        assert "has been cancelled by us" in email_content['Content']['Body'], \
            f"Content does not contain string 'has been cancelled by us'."
    if email_title == admin_email:
        assert "has been cancelled by an admin" in email_content['Content']['Body'], \
            f"Content does not contain string 'has been cancelled by an admin'."
    email_titles.remove(email_title)

gallery(zip(grabber.screens.values(), grabber.captions.values()), row_height="300px")



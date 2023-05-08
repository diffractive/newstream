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

from components import Application
from utils import get_email_count, wait_for_email, get_emails, get_email_by_email_subject, clear_all_emails

import secrets

# +
clear_all_emails()
randstr = secrets.token_hex(6).upper()

email = f'test_user{randstr}@newstream.com'
first_name = 'Test'
last_name = 'User'
password = 'strongpwd'
email_count = get_email_count()
# -

driver = get_webdriver('portal')
grabber = ScreenGrabber(driver)
app = Application(driver)

app.go()
grabber.capture_screen('home_page', 'Home')

app.link('Donation Form').click()
grabber.capture_screen('donation_form', 'Donation Form')

# Cannot go to the signup page without setting a value into the custom amount or choosing a default from selector
app.dropdown('id_donation_amount').select('USD $100')
app.button('Register or Login').click()
grabber.capture_screen('register_login', 'Register or login page')

app.link('Continue with Email Sign up').click()
grabber.capture_screen('sign_up', 'Sign up form')

app.input('id_email').fill(email)
app.input('id_first_name').fill(first_name)
app.input('id_last_name').fill(last_name)
app.input('id_password1').fill(password)
app.input('id_password2').fill(password)
grabber.capture_screen('filled_form', 'Filled signup form')

app.button('Continue').click()
grabber.capture_screen('signed_up', 'Successfully signed up')

# There should be two emails sent, one for admins one for the user
wait_for_email(email_count+1)
email_count += 2

app.label('dropdown-toggle-checkbox').click()
grabber.capture_screen('expanded_menu', 'Expanded user menu')

app.link('header-settings').click()
grabber.capture_screen('profile_udpate_screen', 'Update profile screen')

app.link('Manage Email Addresses').click()
grabber.capture_screen('email_settings', 'Email settings page')

app.button('Re-send Verification').click()
grabber.capture_screen('resend_email_verification', 'Resend email verification')

wait_for_email(email_count)
subject = "Please Confirm Your Email Address"
reg_str = "(?P<url>http://app.newstream.local:8000/en/accounts/confirm-email/[^/]*/)"
url = get_email_by_email_subject(subject, reg_str)
driver.get(url)
grabber.capture_screen('email_confirm', 'Confirm email')

app.button('Confirm').click()
grabber.capture_screen('email_confirmed', 'Email confirmed')

app.label('dropdown-toggle-checkbox').click()
app.link('header-settings').click()
app.link('Manage Email Addresses').click()
grabber.capture_screen('email_verified', 'Email verified')

gallery(zip(grabber.screens.values(), grabber.captions.values()), row_height="300px")

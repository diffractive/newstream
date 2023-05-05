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
# +
clear_all_emails()

email = 'david.donor@diffractive.io'
new_pwd = 'strongpwd'
old_pwd = 'david.donor'
email_count = get_email_count()
# -

driver = get_webdriver('portal')
grabber = ScreenGrabber(driver)
app = Application(driver)

app.go()
grabber.capture_screen('home_page', 'Home')


app.link("header-sign-in").click()
grabber.capture_screen('login_screen', 'Login')


app.link('Forgot Password?').click()
grabber.capture_screen('forgot_password', 'Forgot Password')

app.input('id_email').fill(email)
app.button('Submit').click()
grabber.capture_screen('email_sent', 'Forgot password email sent')

# +
wait_for_email(email_count)
email_content = get_emails()[0]
email_title = email_content['Content']['Headers']['Subject'][0]
email_recipient = email_content['Content']['Headers']['To'][0]

assert email_title == 'Please Reset Your Password', f'Unexpected e-mail found: {email_title}'
assert email_recipient == email, \
    f"Unexpected e-mail recipient {email_recipient}, expected: {email}"
# -

subject = "Please Reset Your Password"
reg_str = "(?P<url>http://app.newstream.local:8000/en/accounts/password/reset/key/[^/]*/)"
url = get_email_by_email_subject(subject, reg_str)
driver.get(url)
grabber.capture_screen('password_reset', 'Reset password form')

app.input('id_password1').fill(new_pwd)
app.input('id_password2').fill(new_pwd)
app.button('Submit').click()
grabber.capture_screen('password_reset_success', 'Password has been reset')

# ## Test

app.link("header-sign-in").click()
grabber.capture_screen('login_screen', 'Login')

app.input('id_login').fill(email)
app.input('id_password').fill(new_pwd)
grabber.capture_screen('filled_login_form', 'Filled Login Form')

app.button('Login').click()
grabber.capture_screen('logged_in', 'Logged in')

# ## Reset info back to default

# Logout
app.label('dropdown-toggle-checkbox').click()
app.link("header-logout").click()
grabber.capture_screen('logged_out', 'Logged out')

app.link("header-sign-in").click()
app.link('Forgot Password?').click()
app.input('id_email').fill(email)
app.button('Submit').click()

wait_for_email(email_count)
subject = "Please Reset Your Password"
reg_str = "(?P<url>http://app.newstream.local:8000/en/accounts/password/reset/key/[^/]*/)"
url = get_email_by_email_subject(subject, reg_str)
driver.get(url)
app.input('id_password1').fill(old_pwd)
app.input('id_password2').fill(old_pwd)
app.button('Submit').click()
grabber.capture_screen('reset_to_default', 'Reset to default')

gallery(zip(grabber.screens.values(), grabber.captions.values()), row_height="300px")

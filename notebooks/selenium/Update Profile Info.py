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
# -

email = 'david.donor@diffractive.io'
password = 'david.donor'
fn_old = 'David'
ln_old = 'Donor'
fn_new = 'Test'
ln_new = 'User'

driver = get_webdriver('portal')
grabber = ScreenGrabber(driver)
app = Application(driver)

app.go()
grabber.capture_screen('home_page', 'Home')


app.link("header-sign-in").click()
grabber.capture_screen('login_screen', 'Login')

app.input('id_login').fill(email)
app.input('id_password').fill(password)
grabber.capture_screen('filled_login_form', 'Filled Login Form')

app.button('Login').click()
grabber.capture_screen('logged_in', 'Logged in')

app.label('dropdown-toggle-checkbox').click()
grabber.capture_screen('expanded_menu', 'Expanded user menu')

app.link('header-settings').click()
grabber.capture_screen('profile_udpate_screen', 'Update profile screen')

app.input('id_first_name').clear()
app.input('id_first_name').fill(fn_new)
app.input('id_last_name').clear()
app.input('id_last_name').fill(ln_new)
app.label('id_opt_in_mailing_list').click()
grabber.capture_screen('filled_form', 'Filled form')

app.button('Submit').click()
grabber.capture_screen('updated_profile', 'Updated profile')

assert app.text('user-fullname').text() == fn_new + ' ' + ln_new

# ## Clean up

app.input('id_first_name').clear()
app.input('id_first_name').fill(fn_old)
app.input('id_last_name').clear()
app.input('id_last_name').fill(ln_old)
app.label('id_opt_in_mailing_list').click()
app.button('Submit').click()
grabber.capture_screen('reset_state', "Reset state to user")

gallery(zip(grabber.screens.values(), grabber.captions.values()), row_height="300px")

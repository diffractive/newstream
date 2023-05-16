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
pwd = 'david.donor'
new_amount = '50'

driver = get_webdriver('portal')
grabber = ScreenGrabber(driver)
app = Application(driver)

app.go()
grabber.capture_screen('home_page', 'Home')

app.link("header-sign-in").click()
grabber.capture_screen('login_screen', 'Login')

app.input('id_login').fill(email)
app.input('id_password').fill(pwd)
grabber.capture_screen('filled_login_form', 'Filled Login Form')

app.button('Login').click()
grabber.capture_screen('logged_in', 'Logged in')

app.label('dropdown-toggle-checkbox').click()
grabber.capture_screen('expanded_menu', 'Expanded menu')

app.link("header-donations").click()
grabber.capture_screen('single_donations', 'My donations page')

app.link('Recurring Donations').click()
grabber.capture_screen('subscriptions', 'Recurring donations')

# 2nd Row
app.label('md2_dropdown-toggle-checkbox2').click()
grabber.capture_screen('open_menu', 'Open subscription menu')

rows = app.table('my-donations-table').rows()
# We need this data_id to fetch the right buttons
data_id = rows[1][5].get_attribute('data-id')
app.button('edit-recurring-donation-wide', data_id).click()
grabber.capture_screen('edit_subscription', 'Edit subscription page')

app.input('id_recurring_amount').clear()
app.input('id_recurring_amount').fill(new_amount)
app.label('Change Billing Cycle to Now').click()
app.button('Update Recurring Donation').click()
grabber.capture_screen('failed_update', 'Failed Update Amount and Cycle')

gallery(zip(grabber.screens.values(), grabber.captions.values()), row_height="300px")



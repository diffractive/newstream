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

# ## Logout flow

app.label('dropdown-toggle-checkbox').click()
grabber.capture_screen('user_menu_expanded', 'Expanded user menu')

app.link("header-logout").click()
grabber.capture_screen('logged_out', 'Logged out')

gallery(zip(grabber.screens.values(), grabber.captions.values()), row_height="300px")

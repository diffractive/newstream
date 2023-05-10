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
old_pwd = 'david.donor'
new_pwd = 'strongpwd'


driver = get_webdriver('portal')
grabber = ScreenGrabber(driver)
app = Application(driver)

app.go()
grabber.capture_screen('home_page', 'Home')


app.link("header-sign-in").click()
grabber.capture_screen('login_screen', 'Login')

app.input('id_login').fill(email)
app.input('id_password').fill(old_pwd)
grabber.capture_screen('filled_login_form', 'Filled Login Form')

app.button('Login').click()
grabber.capture_screen('logged_in', 'Logged in')

app.label('dropdown-toggle-checkbox').click()
grabber.capture_screen('expanded_menu', 'Expanded user menu')

app.link('header-settings').click()
grabber.capture_screen('profile_udpate_screen', 'Update profile screen')

app.link('Security').click()
grabber.capture_screen('security_settings', 'Security screen')

app.link('Change Password').click()
grabber.capture_screen('change_password_screen', 'Change password screen')

app.input('id_oldpassword').fill(old_pwd)
app.input('id_password1').fill(new_pwd)
app.input('id_password2').fill(new_pwd)
grabber.capture_screen('filled_passwords', 'Fill passwords')

app.button('Submit').click()
grabber.capture_screen('updated_passwords', 'Password has been updated')

# ## Test

app.label('dropdown-toggle-checkbox').click()
app.link('header-logout').click()
app.link("header-sign-in").click()
app.input('id_login').fill(email)
app.input('id_password').fill(new_pwd)
app.button('Login').click()
grabber.capture_screen('successfully_logged_in', 'Successfully logged in')

# ## Clean up

app.label('dropdown-toggle-checkbox').click()
app.link('header-settings').click()
app.link('Security').click()
app.link('Change Password').click()
app.input('id_oldpassword').fill(new_pwd)
app.input('id_password1').fill(old_pwd)
app.input('id_password2').fill(old_pwd)
app.button('Submit').click()
grabber.capture_screen('password_reset', 'Password reset')

gallery(zip(grabber.screens.values(), grabber.captions.values()), row_height="300px")

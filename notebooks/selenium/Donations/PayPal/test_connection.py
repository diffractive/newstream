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

import os
import requests
from diffractive.selenium import ScreenGrabber, get_webdriver, notebook_root
from diffractive.selenium.visualisation import gallery
from components import Application

driver = get_webdriver('portal')
grabber = ScreenGrabber(driver)
app = Application(driver)

driver.get(os.getenv('PAYPAL_API_BASE'))
grabber.capture_screen('paypal_sample_api', 'Sample API response')

# should just return a list of users saved on the localpaypal database
req = requests.get(os.getenv('PAYPAL_API_BASE'))
assert req.status_code == 200

gallery(zip(grabber.screens.values(), grabber.captions.values()), row_height="300px")

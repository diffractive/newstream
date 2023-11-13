#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

from diffractive.selenium import wait_element, ScreenGrabber, get_webdriver, notebook_root
from diffractive.selenium.visualisation import gallery

from components import Application

import secrets


# In[2]:


randstr = secrets.token_hex(6).upper()
error_number = "-10-+0"
email = f'test_user{randstr}@newstream.com'
name = 'Test User'


# In[3]:


driver = get_webdriver('portal')
grabber = ScreenGrabber(driver)
app = Application(driver)


# In[4]:


app.go()
grabber.capture_screen('home_page', 'Home')


# In[5]:


app.link('Donation Form').click()
grabber.capture_screen('donation_form', 'Donation Form')


# In[6]:


app.input('id_donation_amount_custom').fill(error_number)
app.input('id_email').fill(email)
app.input('id_name').fill(name)
grabber.capture_screen('error_value', 'Invalid donation amount')


# In[7]:


app.button('Continue as guest').click()
wait_element(driver, '//p[text()="Form Error - Custom Donation amount in Hong Kong Dollar ($):"]')
grabber.capture_screen('form_error', 'Error in donation form')


# In[8]:


gallery(zip(grabber.screens.values(), grabber.captions.values()), row_height="300px")


# In[ ]:





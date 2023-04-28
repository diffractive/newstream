from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import requests
import quopri
import base64
import time

def get_element_by_identifier(driver, element, identifier):
    """
    Get element instance given an identifier
    element: xpath used to identify the html element e.g. "button"
        can also contain a more complex xpath structure depending on the element
    identifier: by default an element's ID but it also has a name, href and text() fallback
    """
    try:
        return driver.find_element(By.XPATH, f'//{element}[@id="{identifier}"]')
    except NoSuchElementException:
        pass
    try:
        return driver.find_element(By.XPATH, f'//{element}[@name="{identifier}"]')
    except NoSuchElementException:
        pass
    try:
        return driver.find_element(By.XPATH, f'//{element}[contains(@href, "{identifier}")]')
    except NoSuchElementException:
        pass

    return driver.find_element(By.XPATH, f'//{element}[text()="{identifier}"]')


def get_children_elements(driver, element):
    """
    Get all children of a specified element type e.g. //select//option
    element: xpath used to identify the html element e.g. "div"
        can also contain a more complex xpath structure depending on the element
    """
    return driver.find_elements(By.XPATH, f'//{element}')

def get_email_count():
    """
    Returns current count of emails in mailhog
    """
    response = requests.get("http://mailhog.newstream.local:8025/api/v2/messages")
    response.encoding = 'utf-8'
    response = response.json()
    
    return len(response['items'])


def wait_for_email(offset=0, timeout=15):
    """
    Returns true when the count of emails is more than "offset", indicating there are new emails than expected
    offset is the amount of emails expected to already be in mailhog
    """
    loaded = False
    start_ts = time.time()
    while not loaded:
        if timeout is not None and time.time() - start_ts > timeout:
            raise TimeoutError("Exceeded %i seconds waiting for e-mail to be received" % (timeout))
        if get_email_count() > offset:
            loaded = True
        else:
            time.sleep(1)


def get_emails(index=0, count=1):
    """
    Returns the email content from mailhog
    TODO: we would like to get the html_content of this so we can have a screenshot of the email
    """

    response = requests.get("http://mailhog.newstream.local:8025/api/v2/messages")
    response.encoding = 'utf-8'
    response = response.json()

    if not response['items']:
        return ''
    
    return response['items'][index:index+count]


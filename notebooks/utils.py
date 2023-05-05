from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import requests
import quopri
import base64
import time
import re

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
    # For links
    try:
        return driver.find_element(By.XPATH, f'//{element}[contains(@href, "{identifier}")]')
    except NoSuchElementException:
        pass
    # For labels
    try:
        return driver.find_element(By.XPATH, f'//{element}[@for="{identifier}"]')
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

def get_email_by_email_subject(subject, reg_str):
    """
    Get url from email given subjeect, and reg_str of what the expected link format should be
    """
    json_object = requests.get(
        "http://mailhog.newstream.local:8025/api/v1/messages"
    )
    response_json = json_object.json()


    for email in response_json:
        if email['Content']['Headers']['Subject'][0] == subject:
            body = email['Content']['Body']
            link_re = re.compile(reg_str)
            url = link_re.search(body).groups()[0]
            clear_email(email['ID'])
            return url

    return ''


def clear_email(message_id):
    """
    Delete email
    """
    json_object = requests.delete(
        "http://mailhog.newstream.local:8025/api/v1/messages/%s" % (message_id)
    )


def clear_all_emails():
    """
    Delete all emails to clear up the email
    """
    json_object = requests.delete(
        'http://mailhog.newstream.local:8025/api/v1/messages'
    )

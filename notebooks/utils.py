from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import requests
import quopri
import base64

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

# +
def get_email_content(index=0):
    """
    Returns the HTML content (base64 encoded) of the most recent email received
    TODO: Should add to selenium runner
    """

    response = requests.get("http://mailhog.newstream.local:8025/api/v2/messages")
    response.encoding = 'utf-8'
    response = response.json()

    if not response['items']:
        return ''

    html_content = next(filter(
        lambda part: part['Headers']['Content-Type'][0].startswith('text/html'),
        response['items'][index]['MIME']['Parts']))
    
    html_content = quopri.decodestring(html_content['Body'])

#     if 'quoted-printable' in html_content['Headers']['Content-Transfer-Encoding']:
#         html_content = quopri.decodestring(html_content['Body'])
#     else:
#         html_content = html_content.encode()

    html_content = base64.b64encode(html_content).decode()
    return html_content
# -



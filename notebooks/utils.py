from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


def get_element_by_identifier(driver, element, identifier):
    """
    Get element instance given an identifier
    element: xpath used to identify the html element e.g. "button"
        can also contain a more complex xpath structure depending on the element
    identifier: by default an element's ID but it also has a name and text() fallback
    """
    try:
        return driver.find_element(By.XPATH, f'//{element}[@id="{identifier}"]')
    except NoSuchElementException:
        pass
    try:
        return driver.find_element(By.XPATH, f'//{element}[@name="{identifier}"]')
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

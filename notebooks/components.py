# +
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException

from utils import get_element_by_identifier, get_children_elements


# -

class Button:
    xpath = 'button'
    def __init__(self, driver, identifier):
        self.element = get_element_by_identifier(driver, self.xpath, identifier)
    
    def click(self):
        self.element.click()    


class Link:
    xpath = 'a'
    def __init__(self, driver, identifier):
        self.element = get_element_by_identifier(driver, self.xpath, identifier)
    
    def click(self):
        self.element.click()


class Dropdown:
    xpath = 'select'
    def __init__(self, driver, identifier):
        self.element = Select(get_element_by_identifier(driver, self.xpath, identifier))
    
    def select(self, value=None, index=0):
        if value:
            try:
                self.element.select_by_value(value)
            except NoSuchElementException:
                pass
            self.element.select_by_visible_text(value)
        else:
            self.element.select_by_index(index)


class Input:
    xpath = 'input'
    def __init__(self, driver, identifier):
        self.element = get_element_by_identifier(driver, self.xpath, identifier)
    
    def fill(self, value):
        self.element.send_keys(value)
    
    def clear(self):
        self.element.clear()


class Application:
    def __init__(self, driver):
        self.driver = driver
        
    #### Components ####
    
    def button(self, identifier):
        return Button(self.driver, identifier)
    
    def link(self, identifier):
        return Link(self.driver, identifier)

    def dropdown(self, identifier):
        return Dropdown(self.driver, identifier)
    
    def input(self, identifier):
        return Input(self.driver, identifier)
    
    #### Methods ####
    
    def go(self, url=''):
        self.driver.get(f'http://app.newstream.local:8000/{url}')



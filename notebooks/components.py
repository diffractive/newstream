# +
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException

from utils import get_element_by_identifier, get_children_elements, get_element_by_data


# -

class Button:
    xpath = 'button'
    def __init__(self, driver, identifier, data=None):
        if data:
            self.element = get_element_by_data(driver, self.xpath, identifier, data)
        else:
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


class Label:
    xpath = 'label'
    def __init__(self, driver, identifier):
        self.element = get_element_by_identifier(driver, self.xpath, identifier)

    def click(self):
        self.element.click()


class Text:
    xpath = 'span'
    def __init__(self, driver, identifier):
        self.element = get_element_by_identifier(driver, self.xpath, identifier)

    def text(self):
        return self.element.text


class Table:
    xpath = "table"
    def __init__(self, driver, identifier):
        self.element = get_element_by_identifier(driver, self.xpath, identifier)

    def row_values(self):
        table_values = []
        for val in get_children_elements(self.element, 'td'):
            # This query returns a bunch of empty values so we should just keep the values
            if val.text:
                table_values.append(val.text)

        return table_values

    def rows(self):
        rows = [row for row in get_children_elements(self.element, 'tr') if row.text]
        row_vals = []
        for row in rows:
            val = [col for col in get_children_elements(row, 'td') if col.text]
            if len(val):
                row_vals.append(val)
        return row_vals


class Application:
    def __init__(self, driver):
        self.driver = driver

    #### Components ####

    def button(self, identifier, data=None):
        return Button(self.driver, identifier, data)

    def link(self, identifier):
        return Link(self.driver, identifier)

    def dropdown(self, identifier):
        return Dropdown(self.driver, identifier)

    def input(self, identifier):
        return Input(self.driver, identifier)

    def label(self, identifier):
        return Label(self.driver, identifier)

    def text(self, identifier):
        return Text(self.driver, identifier)

    def table(self, identifier):
        return Table(self.driver, identifier)

    #### Methods ####

    def go(self, url=''):
        self.driver.get(f'http://app.newstream.local:8000/{url}')



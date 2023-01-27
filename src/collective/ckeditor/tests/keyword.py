from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.command import Command
from SeleniumLibrary.base import keyword
from SeleniumLibrary.keywords import ElementKeywords


@keyword
def mouse_select(self, source, xoffset, yoffset):
    xoffset = int(xoffset)
    yoffset = int(yoffset)
    source_element = self.find_element(source)
    browser = self.driver
    browser.execute_script("arguments[0].scrollIntoView(true);", source_element)
    chain = ActionChains(browser)
    chain.move_to_element_with_offset(source_element, 2, 2)
    chain.click_and_hold()
    chain.move_by_offset(xoffset, yoffset)
    chain.release()
    chain.perform()


@keyword
def mouse_select_element(self, locator):
    element = self.find_element(locator)
    width = element.size['width']
    height = element.size['height']
    browser = self.driver
    browser.execute_script("arguments[0].scrollIntoView(true);", element)
    import time
    time.sleep(0.5)
    chain = ActionChains(browser)
    chain.move_to_element_with_offset(element, -width/2, -height/2)
    chain.click_and_hold()
    chain.move_by_offset(width, height)
    chain.release()
    chain.perform()


@keyword
def scroll_top_left_of_element_into_view(self, locator):
    """Scrolls the element identified by ``locator`` into view.

    See the `Locating elements` section for details about the locator
    syntax.

    New in SeleniumLibrary 3.2.0
    """
    element = self.find_element(locator)
    width = element.size['width']
    height = element.size['height']
    ActionChains(self.driver).move_to_element_with_offset(element, -width/2, -height/2).perform()


setattr(ElementKeywords, 'mouse_select', mouse_select)
setattr(ElementKeywords, 'mouse_select_element', mouse_select_element)
setattr(ElementKeywords, 'scroll_top_left_of_element_into_view',
        scroll_top_left_of_element_into_view)


class TestKeywords(object):

    def dummy_keyword_to_avoid_warning(self):
        pass

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

setattr(ElementKeywords, 'mouse_select', mouse_select)


class TestKeywords(object):

    def dummy_keyword_to_avoid_warning(self):
        pass

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.command import Command
from Selenium2Library import Selenium2Library


def mouse_select(self, source, xoffset, yoffset):
    xoffset = int(xoffset)
    yoffset = int(yoffset)
    source_element = self._element_find(source, True, True)
    browser = self._current_browser()
    # Need to scroll element into view
    # so that i can receive native events
    browser.execute(
        Command.GET_ELEMENT_LOCATION_ONCE_SCROLLED_INTO_VIEW,
        {'id': source_element.id})
    chain = ActionChains(browser)
    chain.move_to_element_with_offset(source_element, 2, 2)
    chain.click_and_hold()
    chain.move_by_offset(xoffset, yoffset)
    chain.release()
    chain.perform()

setattr(Selenium2Library, 'mouse_select', mouse_select)


class TestKeywords(object):

    def dummy_keyword_to_avoid_warning(self):
        pass

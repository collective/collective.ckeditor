from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.command import Command
import SeleniumLibrary
from SeleniumLibrary.base import keyword
from SeleniumLibrary.keywords import ElementKeywords


if int(SeleniumLibrary.__version__[0]) >= 6:
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
        browser = self.driver
        browser.execute_script("arguments[0].scrollIntoView(true);", element)
        import time
        time.sleep(0.5)
        width = element.size['width']
        height = element.size['height']
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
        """
        element = self.find_element(locator)
        width = element.size['width']
        height = element.size['height']
        ActionChains(self.driver).move_to_element_with_offset(element, -width/2, -height/2).perform()


    setattr(ElementKeywords, 'mouse_select', mouse_select)
    setattr(ElementKeywords, 'mouse_select_element', mouse_select_element)
    setattr(ElementKeywords, 'scroll_top_left_of_element_into_view',
            scroll_top_left_of_element_into_view)

elif int(SeleniumLibrary.__version__[0]) == 3:

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
        browser = self.driver
        browser.execute_script("arguments[0].scrollIntoView(true);", element)
        import time
        time.sleep(0.5)
        width = element.size['width']
        height = element.size['height']
        chain = ActionChains(browser)
        chain.move_to_element_with_offset(element, 0, 0)
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
        browser = self.driver
        browser.execute_script("arguments[0].scrollIntoView(true);", element)
        import time
        time.sleep(0.5)


    setattr(ElementKeywords, 'mouse_select', mouse_select)
    setattr(ElementKeywords, 'mouse_select_element', mouse_select_element)
    setattr(ElementKeywords, 'scroll_top_left_of_element_into_view',
            scroll_top_left_of_element_into_view)

else:
    raise NotImplementedError(
        'No support build for Robotframework Library version %s'
        % SeleniumLibrary.__version__
        )


class TestKeywords(object):

    def dummy_keyword_to_avoid_warning(self):
        pass

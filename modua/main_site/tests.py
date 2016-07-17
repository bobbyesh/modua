from django.test import LiveServerTestCase
from selenium import webdriver

class HomePageTests(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_home_page_opens(self):
        """
        The home page opens, and the title contains the word MODUA.
        """
        self.browser.get(self.live_server_url + '/home/')
        assert 'MODUA' in self.browser.title

    def test_register_works(self):
        """
        User clicks register, and goes to a registration screen.
        """
        self.browser.get(self.live_server_url + '/home/')
        link = self.browser.find_element_by_name('registration')
        address = link.get_attribute('href')
        self.browser.get(address)
        assert 'Register' in self.browser.title

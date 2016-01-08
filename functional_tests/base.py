from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
# from .server_tools import reset_database
from .management.commands.create_session import (
    create_pre_authenticated_session
)
from django.conf import settings
import sys
import time

DEFAULT_WAIT = 5


class FunctionalTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if "liveserver" in arg:
                cls.server_host = arg.split("=")[1]
                cls.server_url = "http://" + arg.split("=")[1]
                cls.against_staging = True
                return
        super().setUpClass()
        cls.against_staging = False
        cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        if not cls.against_staging:
            super().tearDownClass()

    def setUp(self):
        if self.against_staging:
            # reset_database(self.server_host)
            pass
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(DEFAULT_WAIT)

    def tearDown(self):
        self.browser.quit()

    def create_pre_authenticated_session(self, email):
        if self.against_staging:
            # session_key = create_session_on_server(self.server_host, email)
            pass
        else:
            session_key = create_pre_authenticated_session(email)

        self.browser.get(self.server_url + "/404_no_such_url/")
        self.browser.add_cookie({
            "name": settings.SESSION_COOKIE_NAME,
            "value": session_key,
            "path": "/"
        })

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id("id_list_table")
        rows = table.find_elements_by_tag_name("tr")
        self.assertIn(row_text, [row.text for row in rows])

    def get_item_input_box(self):
        return self.browser.find_element_by_id("id_text")

    def get_error_element(self):
        return self.browser.find_element_by_css_selector(".has-error")

    def wait_for_element_with_id(self, element_id):
        WebDriverWait(self.browser, timeout=30).until(
            lambda b: b.find_element_by_id(element_id)
        )

    def wait_to_be_logged_in(self, email):
        self.wait_for_element_with_id("logout")
        navbar = self.browser.find_element_by_css_selector(".navbar")
        self.assertIn(email, navbar.text)

    def wait_to_be_logged_out(self, email):
        self.wait_for_element_with_id("login")
        navbar = self.browser.find_element_by_css_selector(".navbar")
        self.assertNotIn(email, navbar.text)

    def wait_for(self, function_with_assertion, timeout=DEFAULT_WAIT):
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                return function_with_assertion()
            except (AssertionError, WebDriverException):
                time.sleep(0.1)
        return function_with_assertion()

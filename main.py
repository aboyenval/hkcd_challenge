
from selenium import webdriver
from bs4 import BeautifulSoup
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
import unittest

class XKCD(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())

    @classmethod
    def tearDownClass(cls) -> None:
        cls.driver.quit()

    def test_main(self):
        """
        Verification of access to the About link on the home page
            Check presence of About link
            Check that about link is clickable
            Check URL
        :return:
        """

        self.driver.get("https://xkcd.com/")

        soup = BeautifulSoup(self.driver.page_source, features="html.parser")
        if soup.find(id="topContainer") is not None and soup.find(id="topLeft") is not None:
            links = self.driver.find_element(by=By.ID, value="topContainer").find_element(by=By.ID, value="topLeft").find_elements(By.TAG_NAME, "a")

            # Click on the About link
            for l in links:
                if l.text == "About":
                    l.click()
                    break

        self.driver.implicitly_wait(10)

        # check URL
        self.assertEqual(self.driver.current_url, "https://xkcd.com/about/", "Cannot open link to About page")

    def _open_about_page(self):
        """
        Open the about page in browser
        :return:
        """
        # open the page
        self.driver.get("https://xkcd.com/about")
        self.soup = BeautifulSoup(self.driver.page_source, features="html.parser")

    def test_title(self):
        """
        Check page title
        :return:
        """
        if self.driver is None or self.driver.current_url != "https://xkcd.com/about":
            self._open_about_page()
        self.assertEqual(self.driver.title, "xkcd - A webcomic")


    def test_background(self):
        """
        Checking the background color outside the text box
        :return:
        """

        if self.driver is None or self.driver.current_url != "https://xkcd.com/about":
            self._open_about_page()

        body = self.driver.find_elements(By.TAG_NAME, "body")[0]

        properties = self.driver.execute_script('return window.getComputedStyle(arguments[0], null);', body)
        background_color = properties['background-color']

        self.assertEqual(background_color, "rgb(150, 168, 200)", "Wrong background color")


    def test_backgound_textbox(self):
        """
        Checking the background color of the text box
        :return:
        """
        if self.driver is None or self.driver.current_url != "https://xkcd.com/about":
            self._open_about_page()

        body = self.driver.find_elements(By.TAG_NAME, "body")[0]

        properties = self.driver.execute_script('return window.getComputedStyle(arguments[0], null);', body)
        background_color = properties['background-color']
        self.assertEqual(background_color, "rgb(150, 168, 200)", "Wrong background color")



    def test_table_width(self):
        """
        Checking the width of the tables
        :return:
        """

        if self.driver is None or self.driver.current_url != "https://xkcd.com/about":
            self._open_about_page()

        driver_tables = self.driver.find_elements(By.TAG_NAME, "table")
        code_tables = self.soup.findAll("table")

        # check tables width using source code analyze and real representation
        self.assertTrue(code_tables[0].has_attr("width"))
        self.assertEqual(int(code_tables[0].attrs["width"]), int(driver_tables[0].size['width']))

        self.assertTrue(code_tables[1].has_attr("width"))
        self.assertEqual(int(code_tables[1].attrs["width"]), int(driver_tables[1].size['width']))


    def test_css(self):
        """
        CSS verification of the text box
        :return:
        """

        if self.driver is None or self.driver.current_url != "https://xkcd.com/about":
            self._open_about_page()

        div = self.driver.find_elements(By.TAG_NAME, "div")[0]

        properties = self.driver.execute_script('return window.getComputedStyle(arguments[0], null);', div)

        self.assertEqual(properties['border-left-width'], "1px")
        self.assertEqual(properties['border-right-width'], "1px")
        self.assertEqual(properties['border-top-width'], "1px")
        self.assertEqual(properties['border-bottom-width'], "1px")

        self.assertEqual(properties['border-left-color'], "rgb(0, 0, 0)")
        self.assertEqual(properties['border-right-color'], "rgb(0, 0, 0)")
        self.assertEqual(properties['border-top-color'], "rgb(0, 0, 0)")
        self.assertEqual(properties['border-bottom-color'], "rgb(0, 0, 0)")

        self.assertEqual(properties['padding-left'], "10px")
        self.assertEqual(properties['padding-right'], "10px")
        self.assertEqual(properties['padding-top'], "10px")
        self.assertEqual(properties['padding-bottom'], "10px")

        self.assertEqual(properties['margin-left'], "5px")
        self.assertEqual(properties['margin-right'], "5px")
        self.assertEqual(properties['margin-bottom'], "5px")


    def test_scrolling(self):
        """
        Checking the possibility of scrolling
        :return:
        """

        if self.driver is None or self.driver.current_url != "https://xkcd.com/about":
            self._open_about_page()

        # get the page height
        html = self.driver.find_elements(By.TAG_NAME, "html")[0]
        html_height = html.size['height']

        # get the screen height
        window_height = self.driver.execute_script('return window.innerHeight')

        scrollpos_initial = self.driver.execute_script("return document.body.scrollTop")
        self.assertEqual(scrollpos_initial, 0)

        # Scroll down to bottom
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        scrollpos_new = self.driver.execute_script("return document.body.scrollTop")

        scrollpos_target = int(scrollpos_new) + int(window_height)

        # check if we can scroll to max height with tolerance: 1px
        self.assertLessEqual(abs(int(html_height)-scrollpos_target), 1, "Cannot scroll to max height")



    def test_link_back(self):
        """
        Checking the link back to the main menu
        :return:
        """

        if self.driver is None or self.driver.current_url != "https://xkcd.com/about":
            self._open_about_page()

        # search for the links
        links = self.soup.findAll("a")
        found = False
        for link in links:
            if link.has_attr("href") and link.attrs['href'] == "/":
                found = True

        self.assertTrue(found, "Cannot found link to back menu")
import os
import unittest
from base_test import BaseTest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

class NavigationTest(BaseTest, unittest.TestCase):

    def job_name(self):
        return 'Navigation test'

    def test_navigation(self):
        self.driver.get('http://localhost:8000/1005-5/2012-12121')
        WebDriverWait(self.driver, 30).until(
            lambda driver: driver.find_element_by_css_selector('html.js'))

        self.driver.execute_script('poffset = document.getElementById("1005-5-b-2").offsetTop')
        self.driver.execute_script('window.scrollTo(0, poffset)')
        # wayfinding header should update
        WebDriverWait(self.driver, 10).until(
            lambda driver: driver.find_element_by_xpath('//*[@id="active-title"]').text in 
            (u'\u00A71005.5(b)(1)', u'\u00A71005.5(b)'))

        fwd_link = self.driver.find_element_by_xpath('//*[@id="1005-5"]/nav/ul/li[2]/a')
        fwd_link.click()
        # should navigate to next section
        WebDriverWait(self.driver, 30).until(
            lambda driver: driver.find_element_by_id('1005-6'))

        self.driver.back()

        # should go back to 1005-5
        self.driver.find_element_by_xpath('//*[@id="1005-5"]')
        back_link = self.driver.find_element_by_xpath('//*[@id="1005-5"]/nav/ul/li[1]/a')
        back_link.click()
        # should navigate to 1005-4
        WebDriverWait(self.driver, 30).until(
            lambda driver: driver.find_element_by_id('1005-4'))

if __name__ == '__main__':
    unittest.main()

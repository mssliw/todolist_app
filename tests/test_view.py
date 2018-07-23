import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class TestToDoList(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(executable_path='/home/magda/chromedriver')

    def test_view(self):
        driver = self.driver
        driver.get("http://localhost:5000/")
        self.assertIn("To do list app", driver.title)

        assert "No results found." not in driver.page_source

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
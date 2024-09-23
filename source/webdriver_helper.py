import selenium
from itertools import chain
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options

class WebDriverHelper:
    def __init__(self):
        options = Options()
        options.add_argument("--start-maximized")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        # Uncomment to not see the window process while scrapping
        # options.add_argument("--headless=new")
        options.ignore_certificate_errors = True

        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(5)

    def accept_cookies(self):
        """Accept cookies. """

        try:
            accept_button = self.driver.find_element(By.XPATH, 
            "//*[@id='didomi-notice-agree-button']")
            accept_button.click()
        except selenium.common.exceptions.NoSuchElementException:
            pass

    def close_ads(self):
        """" Close the ads of the page. """
        try:
            close_add = self.driver.find_element(By.XPATH, 
            "//*[@src='https://secure-ds.serving-sys.com/BurstingCachedScripts//HTML5FactoryFiles/ExpandFS/1_0_0/default_close']")
            close_add.click()
        except selenium.common.exceptions.NoSuchElementException:
            pass

    def scroll_page(self):
        """ Scroll page 1300 pixels, to a fully-load of the page."""

        ActionChains(self.driver)\
        .scroll_by_amount(0, 1300)\
        .perform()

    def finalize(self):
        """ Quit the driver"""
        self.driver.quit()


    def get_all_cities(self):
        """Get all Spain cities scrapping them. """

        cities_url = "https://www.eltiempo.es/espana"
        self.driver.get(cities_url) 
        self.accept_cookies()

        comm_and_cities = self.driver.find_element(By.XPATH,
        "//*[@id='main']/div[4]/div/section[2]/article/div")

        cities = comm_and_cities.find_elements(By.XPATH,  "//*[@class='drop-down closed']")
        cities = [city.text.split('\n')[0:] for city in cities]
        cities = list(chain.from_iterable(cities))

        return cities

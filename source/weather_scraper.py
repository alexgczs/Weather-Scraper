import selenium
import tqdm
import pandas as pd
from selenium.webdriver.common.by import By
from calendar import month_name, different_locale
from webdriver_helper import WebDriverHelper


class WeatherScraper(WebDriverHelper):
    """
    Class to scrape meteorological data from the website El Tiempo.
    The class initializes the structures in which the datasets are stored
    and defines the scraping method.
    This class inherits from the WebDriverHelper class, which contains the logic
    for page handling.

    Args:
        city (optional): The city(ies) for which meteorological data is to be scraped.
        If not specified, data for all cities on <eltiempo.es/espana> will be scraped.
        These cities will be obtained by scraping.

    Attributes:
        places: Sites from which meteorological information is to be scraped,
        indicated in the argument. If 'all' is specified, the names of the cities 
        from <eltiempo.es/espana> will be scraped.

        months: List that contains the names of the months in Spanish.
        Stored as an attribute for easy iteration over the months.

        dataset1: Dataframe that acts as a data structure to store
        the first dataset.

        dataset2: Dataframe that acts as a data structure to store
        the second dataset.
    """

    def __init__(self, city='all'):
        # Inherit from WebDriverHelper
        super().__init__()
        # If we want all places, we scrape the names with get_all_comm (in webdriverhelper)
        self.places = self.get_all_cities() if city == 'all' else [city]

        # Initialize the months in Spanish to iterate over them in scraping
        with different_locale('es'):
            self.months = [month_name[i].capitalize() for i in range(1, 13)]

        # Initialize the structures for storing datasets
        self.dataset1 = pd.DataFrame(columns=["day", "week day", "temperature_max",
                                              "temperature_min", "rain", "snow",
                                              "wind", "sunrise", "sunset", "place"])

        self.dataset2 = pd.DataFrame(columns=["month", "avg_temp", "max_temp",
                                              "min_temp", "rain_days", "rain_accum",
                                              "avg_wind", "place"])

    def scrape_weather_data(self):
        """
        Main scraping function, works as a launcher.
        """

        # Initialize a bar to indicate scraping progress
        progress_bar = tqdm.tqdm(total=len(self.places), desc="Scraping progress")

        # Scrape the data for each city
        for city in self.places:
            self.driver.get(f"https://www.eltiempo.es/{city}.html")
            self.accept_cookies()
            self.close_ads()

            # Data for the first dataset
            try: 
                table = self.driver.find_element(By.XPATH, "//*[@id='cityPoisTable']//table")
                data = get_weather_data_from_table(table, city)

                for weather_data in data:
                    self.dataset1 = pd.concat([self.dataset1, pd.DataFrame([weather_data])],
                                              ignore_index=True)

            except selenium.common.exceptions.NoSuchElementException:
                pass

            # Scroll down the page to finish loading
            self.scroll_page()

            try:
                # Data for the second dataset
                second_tab = self.driver.find_element(By.XPATH, "//div[@class='card']")
                # Find the dropdown that contains the months
                dropdown = second_tab.find_element(By.XPATH,
                    "//*[@id='main']/div[4]/div/main/section[4]/section/div/div/article[1]/div/div/div")
                data = {}
                # For each month
                for month in self.months:
                    # Expand the options and click on each month
                    dropdown.click()
                    month_elem = self.driver.find_element(By.XPATH, f"//*[@id='month_average_chosen']/div/ul/li[text()='{month}']")
                    month_elem.click()
                    # Scrape the data for the specific month
                    new_data = get_weather_data_monthly(second_tab, city, month)
                    self.dataset2 = pd.concat([new_data, self.dataset2], ignore_index=True)

            except selenium.common.exceptions.NoSuchElementException:
                pass
            # The progress bar advances
            progress_bar.update(1)
        # Close the webDriver
        self.finalize()

    def save_datasets(self):
        """
        Save the 2 datasets to memory.
        """

        self.dataset1.to_csv("dataset/dataset1.csv", index=False)
        self.dataset2.to_csv("dataset/dataset2.csv", index=False)

# 2 auxiliary functions: One for each dataset

def get_weather_data_from_table(table, city):
    """
    Given the structure from which to scrape data, it retrieves and returns it
    through a generator.
    """

    # Get the data for the 2 weeks offered by the page
    for idx in range(2, 16):
        day_header = table.find_element(By.XPATH, f"thead/tr/th[{idx}]")
        data = {
            "day": day_header.find_element(By.XPATH, "div[1]/span").text,
            "week day": day_header.find_element(By.XPATH, "span").text,
            "temperature_max": day_header.find_element(
                By.XPATH, "div[2]/div[1]/span"
            ).text,
            "temperature_min": day_header.find_element(
                By.XPATH, "div[2]/div[2]/span"
            ).text,
            "rain": table.find_element(By.XPATH, f"tbody/tr[4]/td[{idx}]").text,
            "snow": table.find_element(By.XPATH, f"tbody/tr[5]/td[{idx}]").text,
            "wind": table.find_element(By.XPATH, f"tbody/tr[6]/td[{idx}]").text,
            "sunrise": table.find_element(By.XPATH, f"tbody/tr[7]/td[{idx}]").text,
            "sunset": table.find_element(By.XPATH, f"tbody/tr[8]/td[{idx}]").text,
            "place": city
        }
        yield data


def get_weather_data_monthly(second_tab, city, month):
    """
    Get meteorological data by month, given a structure and site.
    """

    data = {
        "month": month,
        "avg_temp": second_tab.find_element(By.XPATH, "//span[@id='temp']").text,
        "max_temp": second_tab.find_element(By.XPATH, "//span[@id='temp-max']").text,
        "min_temp": second_tab.find_element(By.XPATH, "//span[@id='temp-min']").text,
        "rain_days": second_tab.find_element(By.XPATH, "//span[@id='rain-days']").text,
        "rain_accum": second_tab.find_element(By.XPATH, "//span[@id='rain']").text,
        "avg_wind": second_tab.find_element(By.XPATH, "//span[@id='wind']").text,
        "place": city
    }
    return pd.DataFrame(data, index=[0])

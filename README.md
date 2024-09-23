# Web scraping from eltiempo.es

## Description

This code performs web scraping processes on the [El Tiempo](https://www.eltiempo.es/) website.

Through web scraping, two datasets are constructed, which are located in the _dataset_ folder.


## Structure

- **/dataset:** Contains the two datasets detailed in the next section
    - dataset1.csv
    - dataset2.csv

- **/images:** Contains the images that accompany this file.

- **/Other resources**:
    - CheckSeleniumAgent.ipynb: Jupyter notebook that checks which agent Selenium is using and proposes a method to change it to a specific one.

- **/source**:
    - main.py: File that runs the script. Optionally, we can pass a string argument corresponding to a city for which we want to extract the data. If no argument is passed, it will default to "all", scraping data from all cities on [this El Tiempo page](https://www.eltiempo.es/espana).
    - web_driver_helper.py: Class that creates methods to manage webDriver-webpage interaction.
    - weather_scraper.py: Contains the WeatherScraper class, an object used for scraping. It inherits from the WebDriverHelper class and is responsible for extracting the data and saving the datasets.

- **requirements.txt**: Contains the package versions needed to run the script.

# Web scraping from eltiempo.es

## Description

This code performs web scraping processes on the [El Tiempo](https://www.eltiempo.es/) website.

Through web scraping, two datasets are constructed, which are located in the _dataset_ folder.


## Structure

- **/dataset:** Contains the two datasets detailed in the next section
    - daily_temperature_spain (11-2023).csv
    - monthly_temperature_spain (1996-2023).csv

- **/Other resources**:
    - CheckSeleniumAgent.ipynb: Jupyter notebook that checks which agent Selenium is using and proposes a method to change it to a specific one.

- **/source**:
    - main.py: File that runs the script. Optionally, we can pass a string argument corresponding to a city for which we want to extract the data. If no argument is passed, it will default to "all", scraping data from all cities on [this El Tiempo page](https://www.eltiempo.es/espana).
    - web_driver_helper.py: Class that creates methods to manage webDriver-webpage interaction.
    - weather_scraper.py: Contains the WeatherScraper class, an object used for scraping. It inherits from the WebDriverHelper class and is responsible for extracting the data and saving the datasets.

- **requirements.txt**: Contains the package versions needed to run the script.

## About the datasets

### daily_temperature_spain (11-2023).csv:
 It consists of 561 observations and 10 variables per observation. The dataset contains observations about future weather predictions for cities in Spain. The data in this dataset is from November 12 to November 25, 2023. Below is a small extract of them:

 o	**day**: Describes the day to which the observation refers. It is saved in the form "DD MM" (where DD is the day number and MM is the month).

o	**week day**: Describes the day of the week to which the observation refers (Monday, Tuesday, Wednesday...). On the day the data is extracted, this field takes the value "Today," and the next day takes the value "Tomorrow." This variable should be cleaned by replacing "Today" and "Tomorrow" with the actual weekday.

o	**temperature_max**: Records the maximum temperature (in degrees) forecasted for the specific day and location to which the observation refers.

o	**temperature_min**: Records the minimum temperature (in degrees) forecasted for the specific day and location to which the observation refers.

o	**rain**: Indicates the amount of rain (in millimeters per square meter) forecasted for the specific day and location to which the observation refers.

o	**snow**: Indicates the amount of snow (in millimeters of depth) forecasted for the specific day and location to which the observation refers.

o	**wind**: Indicates the wind speed (in kilometers per hour) forecasted for the specific day and location to which the observation refers.

o	**sunrise**: Refers to the time sunrise is expected.

o	**sunset**: Refers to the time sunset is expected.

o	**place**: The city to which the observation refers.

### monthly_temperature_spain (1996-2023).csv

It consists of 481 observations and 8 variables per observation. The dataset contains observations representing the average monthly climate for each city. Since the data in this dataset are monthly averages, we can say that the time period covered by the data spans from the creation of the website (1996) to 2023. Below is a small extract of them:

o	**month**: Refers to the month being described.

o	**temp_media**: The average of the average temperatures for that month (for the specific location being described).

o	**temp_max**: The average of the maximum temperatures for that month (for the specific location being described).

o	**temp_min**: The average of the minimum temperatures for that month (for the specific location being described).

o	**rain_days**: Average number of rainy days for that month (for the specific location being described).

o	**rain_accum**: Average rain accumulation for that month (for the specific location being described).

o	**avg_wind**: Average wind speed for that month (for the specific location being described).

o	**place**: The city to which the observation refers.
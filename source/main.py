import argparse
import weather_scraper

if __name__ == "__main__":
    # Accept a specific city as an argument to scrape the data
    # If not specified, data from all cities on <eltiempo.es/espana> is scraped
    parser = argparse.ArgumentParser()
    parser.add_argument("--city", nargs="?", const="all", default='all')
    args = parser.parse_args()

    # Data scraping
    scraper = weather_scraper.WeatherScraper(args.city)
    print('\nScraping has started')
    scraper.scrape_weather_data()
    scraper.save_datasets()
    print('\nScraping successfully completed')

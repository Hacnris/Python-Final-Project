
from html.parser import HTMLParser
import urllib.request
from datetime import datetime

class WeatherScraper(HTMLParser):
    """This module will scrape weather data from station 27174 for max, min and mean temperatures."""

    def __init__(self):
        """Initializes an instance of the WeatherScraper class."""
        try:
            HTMLParser.__init__(self)
            self.tbody = False
            self.tr = False
            self.td = False
            self.last_page = False

            self.counter = 0
            self.month_counter = 0

            self.daily_temps = {}
            self.weather = {}

            self.row_date = ""

        except Exception as error:
            print("Exception happened:", error)

    def handle_starttag(self, tag, attrs):
        """Handles the starttag event."""

        try:
            if tag.__eq__("tbody"):
                self.tbody = True

            if tag.__eq__("tr") and self.tbody is True:
                self.tr = True

            if tag.__eq__("td") and self.tr is True:
                self.counter += 1
                self.td = True

            # Format the abbr tag to a desired output.
            if tag.__eq__("abbr") and self.tr is True:
                self.row_date = str(datetime.strptime(attrs[0][1], "%B %d, %Y").date())

            #Detects the last page from return data.
            if len(attrs) == 2:
                if attrs[1][1] == "previous disabled":
                    self.last_page = True

        except Exception as error:
            print("Exception happened:", error)

    def handle_endtag(self, tag):
        """Handles the endtag event."""

        try:
            if tag.__eq__("td"):
                self.td = False

            if tag.__eq__("tr"):
                self.counter = 0
                self.tr = False

        except Exception as error:
            print("Exception happened:", error)

    def handle_data(self, data):
        """Handles the data event."""
        try:
            cast = False
            if data.__eq__("Sum"):
                self.tbody = False

            #Generates daily_temps dictionary.
            if self.td is True and self.counter <= 3 and self.tbody is True:
                try:
                    tempCast = float(data)
                    cast = True
                except Exception as error:
                    cast = False
                if(cast):
                    keys = ['Max', 'Min', 'Mean']
                    self.daily_temps[keys[self.counter - 1]] = data

            #Generates weather dictionary.
            if self.counter == 3 and cast:
                self.weather[self.row_date] = self.daily_temps
                self.daily_temps = self.daily_temps.copy()

        except Exception as error:
            print("Exception happened:", error)

    def get_data(self) -> dict:
        """Scrapes each month and year, returns a dictionary containing the required weather data."""

        try:
            today  = datetime.now()

            while self.last_page is False:

                try:
                    url = (f'https://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174&timeframe=2&StartYear=1840&EndYear=2018&Day={today.day}&Year={today.year}&Month={today.month}#')

                    if today.month == 1:
                        today = today.replace(month=12)
                        today = today.replace(year=today.year-1)

                    else:
                        today = today.replace(month=today.month-1)

                    with urllib.request.urlopen(url) as response:
                        html = str(response.read())

                    self.month_counter += 1

                    self.feed(html)

                except Exception as error:
                    print("Exception happened:", error)

            return self.weather

        except Exception as error:
            print("Exception happened:", error)

    def update_scrape(self, end_date:datetime) -> dict:
        """Only scrapes the data till it reaches the provided end month and year."""

        try:
            today = datetime.now().date()
            completed = False

            while not completed:

                try:
                    if(end_date.month == today.month) and (end_date.year == today.year):
                        completed = True

                    url = (f'https://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174&timeframe=2&StartYear=1840&EndYear=2018&Day={today.day}&Year={today.year}&Month={today.month}#')

                    if today.month == 1:
                        today = today.replace(month=12)
                        today = today.replace(year=today.year-1)

                    else:
                        today = today.replace(month=today.month-1)

                    with urllib.request.urlopen(url) as response:
                        html = str(response.read())

                    self.month_counter += 1

                    self.feed(html)

                except Exception as error:
                    print("Exception happened:", error)

            return self.weather

        except Exception as error:
            print("Exception happened:", error)

#Test Program.
if __name__ == "__main__":
    test = WeatherScraper().get_data()
    for k, v in test.items():
        print(k, v)

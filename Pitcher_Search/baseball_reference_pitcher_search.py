from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import re
import chromedriver_autoinstaller
from selenium.common.exceptions import WebDriverException


options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--headless") # using headless chrome option for speed
# options.add_argument("--auto-open-devtools-for-tabs") # hoping that this will get rid of the full screen pop up ads

service = Service(executable_path="C:/pitcherPredictions/chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)




class Pitcher():
    def __init__(self, name, driver):
        self.name = name
        self.url = "https://www.baseball-reference.com/"
        self.driver = driver
        self.searchBar = None
        self.openPlayerPage() # upon instantiation - the standard player page will get opened for further investigation

    def openPlayerPage(self):
        self.driver.get(self.url)
        self.clickSearch()  # clicking on the search bar
        self.searchBar.send_keys(self.name)
        self.searchBar.send_keys(Keys.RETURN)

    def clickSearch(self):
        self.searchBar = self.driver.find_element(By.XPATH, '//*[@id="header"]/div[3]/form/div/div/input[2]')
        self.searchBar.click()

    def currentURL(self):
        return self.driver.current_url()

    def gettingPlayerID(self):  # Get the player id from the URL to search other cast off webpages
        url = self.driver.current_url
        pattern = r'/players/.+?/(.+?)\.shtml' # Using regular expression to extract ID from original URL for player
        match = re.search(pattern, url)
        if match:
            result = match.group(1)
            return result
        else:
            result = "Could not find player"
            return result

    def thisYearPage(self): # gets the URL of this years game logs for that pitcher
        idPartOfURL = self.gettingPlayerID()
        foundationURL = "https://www.baseball-reference.com/players/gl.fcgi?id="
        fullURL = foundationURL + idPartOfURL + "&year=2023&t=p"
        return fullURL

    def newYearNavigation(self):  # navigates driver to open the game log webpage for the player
        self.driver.get(self.thisYearPage())

    def gettingGamgeLogs(self):  # navigates and scrapes the game logs and returns them in a pandas dataframe

        self.newYearNavigation() # Opening the page that contains the game logs for the player
        table = self.driver.find_element(By.XPATH, "//table[@id='pitching_gamelogs']")

        # Get all rows within the table.
        rows = table.find_elements(By.TAG_NAME, "tr")
        # Extract column names (header cells) from the first row.
        header_row = rows[0]
        columns = header_row.find_elements(By.TAG_NAME, "th")
        column_names = [column.text for column in columns]
        column_names.pop(0)
        # Initialize an empty list to store the table data (excluding the header row).
        table_data = []

        # Loop through each row (excluding the header row) and extract data from cells.
        for row in rows[1:]:
            # Find all cells within the row (replace the 'td_locator' with 'td' depending on your table structure).
            cells = row.find_elements(By.TAG_NAME, "td")

            # Extract data from each cell and store it in a row_data list.
            row_data = [cell.text for cell in cells]

            # Append the row_data to the table_data list.
            table_data.append(row_data)


        df = pd.DataFrame(table_data, columns=column_names)

        return df  # This returns data frame of all stats from the given players game log in the 2023 season

# pitcher = Pitcher("Shohei Ohtani", driver)
# pitcher.openPlayerPage()
# pitcher.newYearNavigation()
# gameLogs = pitcher.gettingGamgeLogs()
#
# print(gameLogs['SO'])
# # pitcher.gettingPlayerID()
#
# input("Press Enter to exit...")


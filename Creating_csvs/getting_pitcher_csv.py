from Pitcher_Search import baseball_reference_pitcher_search as ps
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import pandas as pd
import os


options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--headless") # using headless chrome option for speed
# options.add_argument("--auto-open-devtools-for-tabs") # hoping that this will get rid of the full screen pop up ads


# UPDATE THIS TO PATH TO LOCATION OF CURRENT VERSION OF CHROMEDRIVER
service = Service(executable_path="C:/pitcherPredictions/chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)



pitcher_name = input("Enter a pitcher name: ")

pitcher = ps.Pitcher(pitcher_name, driver)  # creating a pitcher object for the given pitcher name
# pitcher.openPlayerPage()
# pitcher.newYearNavigation()
dataframe = pitcher.gettingGamgeLogs()   # store the dataframe of stats (these are the game logs from the 2023 season


current_directory = os.path.dirname(os.path.abspath(__file__))

fileName = 'player_standard_pitching.csv'  # can change this to whatever the file name needs to be

#constuct the path to the CSV file
csv_file_path = 'C:/pitcherPredictions/csvs/' + fileName

data = pd.read_csv(csv_file_path)




from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

service = Service(executable_path="C:/pitcherPredictions/chromedriver.exe")
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
# options.add_argument("--headless") # using headless chrome option for speed
options.add_argument("--auto-open-devtools-for-tabs") # hoping that this will get rid of the full screen pop up ads
driver = webdriver.Chrome(service=service, options=options)

# driver.get("https://www.thebaseballcube.com/content/box_date/20230330/")

ALL_PLAYER_STATS = []

# This function creates the URLs, and sends them for the site to be navigated
def creatingURLs(driver):
    date_extensions = [
        "20230330", "20230331", "20230401", "20230402", "20230403", "20230404", "20230405", "20230406", "20230407","20230408",
        "20230409", "20230410", "20230411", "20230412", "20230413", "20230414", "20230415", "20230416", "20230417","20230418",
        "20230419", "20230420", "20230421", "20230422", "20230423", "20230424", "20230425", "20230426", "20230427","20230428",
        "20230429", "20230430", "20230501", "20230502", "20230503", "20230504", "20230505", "20230506", "20230507","20230508",
        "20230509", "20230510", "20230511", "20230512", "20230513", "20230514", "20230515", "20230516", "20230517","20230518",
        "20230519", "20230520", "20230521", "20230522", "20230523", "20230524", "20230525", "20230526", "20230527","20230528",
        "20230529", "20230530", "20230531", "20230601", "20230602", "20230603", "20230604", "20230605", "20230606","20230607",
        "20230608", "20230609", "20230610", "20230611", "20230612", "20230613", "20230614", "20230615", "20230616","20230617",
        "20230618", "20230619", "20230620", "20230621", "20230622", "20230623", "20230624", "20230625", "20230626","20230627",
        "20230628", "20230629", "20230630", "20230701", "20230702", "20230703", "20230704", "20230705", "20230706","20230707",
        "20230708", "20230709", "20230710", "20230711", "20230712", "20230713", "20230714", "20230715", "20230716","20230717",
        "20230718", "20230719", "20230720", "20230721", "20230722", "20230723", "20230724", "20230725", "20230726","20230727",
        "20230728", "20230729", "20230730", "20230731",
    ]
    urlFoundation = "https://www.thebaseballcube.com/content/box_date/"
    for date in date_extensions:
        print(date)
        fullURL = urlFoundation + date + "/"
        navigatingWebsite(driver, fullURL)

def navigatingWebsite(driver, url):
    driver.get(url)

    # Getting all 'box' href elements to be clicked on
    td_elements = driver.find_elements(By.XPATH, "//td[@class='align_left']//a[contains(text(), 'box')]")
    for i in range(len(td_elements)):
        td_elements = driver.find_elements(By.XPATH, "//td[@class='align_left']//a[contains(text(), 'box')]")
        driver.execute_script("window.scrollBy(0, 500);")
        td_elements[i].click()
        driver.execute_script("window.scrollBy(0, 500);")
        time.sleep(5)
        gettingStats(driver)
        print("end of that game")
        driver.back()   # returning to the main game page to get next element

def gettingStats(driver):
    wait = WebDriverWait(driver, 20)


    awayTeamStarterName = driver.find_element(By.XPATH, "/html/body/main/section/div[5]/div[1]/table/tbody/tr[2]/td[2]/a").get_attribute("innerHTML")
    awayTeamOpponents = driver.find_element(By.XPATH, "/html/body/main/section/div[2]/table/tbody/tr[3]/td[1]/a").get_attribute("innerHTML")
    awayTeamStarterStrikeouts = driver.find_element(By.XPATH, "/html/body/main/section/div[5]/div[1]/table/tbody/tr[2]/td[9]").get_attribute("innerHTML")
    awayTeamStarterInnings = driver.find_element(By.XPATH, "/html/body/main/section/div[5]/div[1]/table/tbody/tr[2]/td[4]").get_attribute("innerHTML")  # this will be a float

    homeTeamStarterName = driver.find_element(By.XPATH, "/html/body/main/section/div[5]/div[2]/table/tbody/tr[2]/td[2]/a").get_attribute("innerHTML")
    homeTeamOpponents = driver.find_element(By.XPATH, "/html/body/main/section/div[2]/table/tbody/tr[2]/td[1]/a").get_attribute("innerHTML")
    homeTeamStarterStrikeouts = driver.find_element(By.XPATH, "/html/body/main/section/div[5]/div[2]/table/tbody/tr[2]/td[9]").get_attribute("innerHTML")
    homeTeamStarterInnings = driver.find_element(By.XPATH, "/html/body/main/section/div[5]/div[2]/table/tbody/tr[2]/td[4]").get_attribute("innerHTML")  # this will be a float

    data_dict = [
        {"Player Name": awayTeamStarterName, "Days Opponent": awayTeamOpponents, "Strikeouts": awayTeamStarterStrikeouts, "Innings Pitched": awayTeamStarterInnings},
        {"Player Name": homeTeamStarterName, "Days Opponent": homeTeamOpponents, "Strikeouts": homeTeamStarterStrikeouts, "Innings Pitched": homeTeamStarterInnings}
    ]

    print("Adding to ALL_PLAYER_STATS")
    ALL_PLAYER_STATS.append(data_dict)

    # TESTING PURPOSES
    #
    # print(awayTeamStarterName)
    # print(awayTeamStarterStrikeouts)
    # print(awayTeamStarterInnings)
    # print(homeTeamStarterStrikeouts)
    # print(homeTeamStarterInnings)



# Converting the list of dictionaries to a csv
def convertToCsv():
    df = pd.DataFrame(ALL_PLAYER_STATS)

    df.to_csv("player_game_by_game_stats.csv", index=False)







# navigatingWebsite(driver)

# gettingStats(driver)

creatingURLs(driver)
convertToCsv()


driver.close()
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
import time
from pprint import pprint
import yaml


# Force Twitch player
OVERRIDDES = {
    "https://lolesports.com/live/lck_challengers_league":"https://lolesports.com/live/lck_challengers_league/lckcl",
    "https://lolesports.com/live/lpl":"https://lolesports.com/live/lpl/lpl",
    "https://lolesports.com/live/lck":"https://lolesports.com/live/lck/lck",
    "https://lolesports.com/live/lec":"https://lolesports.com/live/lec/lec",
    "https://lolesports.com/live/lcs":"https://lolesports.com/live/lcs/lcs"
}
CONFIG_LOCATION="config.yaml"

def getLiveMatches(driver):
    matches = []
    elements = driver.find_elements(by=By.CSS_SELECTOR, value="a.match.live")
    for element in elements:
        matches.append(element.get_attribute("href"))
    return matches

def readConfig(filepath):
    with open(filepath, "r") as f:
        return yaml.safe_load(f)

# def logIn(driver, username, password):
#     driver.get("https://lolesports.com/")
#     time.sleep(2)
#     pass

#https://auth.riotgames.com/login
###################################################
log = logging.getLogger("League of Poro")
log.setLevel('DEBUG')
chromedriver_autoinstaller.install()

hasValidConfig = False
username = None
password = None
try:
    config = readConfig(CONFIG_LOCATION)
    hasValidConfig = True
    pprint(config)
except FileNotFoundError:
    log.warn("Configuration file not found. IGNORING...")
except (yaml.scanner.ScannerError, yaml.parser.ParserError) as e:
    log.warn("Invalid configuration file. IGNORING...")

options = webdriver.ChromeOptions() 
driver = webdriver.Chrome(options=options)
driver.get("https://lolesports.com/")
time.sleep(2)

while not driver.find_elements(by=By.CSS_SELECTOR, value="div.riotbar-summoner-name"):
    log.info("Waiting for log in")
    time.sleep(5)
log.info("Okay, we're in")
time.sleep(5)

currentWindows = {}
originalWindow = driver.current_window_handle

while True:
    driver.switch_to.window(originalWindow) # just to be sure
    time.sleep(5)
    liveMatches = getLiveMatches(driver)
    log.info(f"{len(liveMatches)} matches live")

    # Close windows finished matches
    toRemove = []
    for k in currentWindows.keys():
        if k not in liveMatches:
            log.info(f"{k} has finished")
            driver.switch_to.window(currentWindows[k])
            driver.close()
            toRemove.append(k)
            driver.switch_to.window(originalWindow)
            time.sleep(5)
    for k in toRemove:
        currentWindows.pop(k, None)

    # Open new live matches
    newLiveMatches = set(liveMatches) - set(currentWindows.keys())
    log.info(f"{len(newLiveMatches)} new matches")
    for match in newLiveMatches:
        driver.switch_to.new_window('tab')
        time.sleep(2)
        currentWindows[match] = driver.current_window_handle
        if match in OVERRIDDES:
            url = OVERRIDDES[match]
            log.info(f"Overriding {match} to {url}")
        else:
            url = match
        driver.get(url)
        time.sleep(30)

    driver.switch_to.window(originalWindow)
    time.sleep(900)




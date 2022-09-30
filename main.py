import logging
import logging.config
from this import d
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
import yaml
import argparse
from datetime import datetime, timedelta

# Functions
from Functions.Setup.Config import readConfig

# Classes
from Classes.Setup.Login import Login
from Classes.Setup.Webdriver import Webdriver
from Classes.Setup.Logger import Logger
from Classes.EsportCapsuleFarmer.Rewards import Rewards
from Classes.EsportCapsuleFarmer.Match import Match
from Classes.EsportCapsuleFarmer.Twitch import Twitch

# Force Twitch player
OVERRIDES = {
    "https://lolesports.com/live/lck_challengers_league":"https://lolesports.com/live/lck_challengers_league/lckcl",
    "https://lolesports.com/live/lpl":"https://lolesports.com/live/lpl/lpl",
    "https://lolesports.com/live/lck":"https://lolesports.com/live/lck/lck",
    "https://lolesports.com/live/lec":"https://lolesports.com/live/lec/lec",
    "https://lolesports.com/live/lcs":"https://lolesports.com/live/lcs/lcs",
    "https://lolesports.com/live/lco":"https://lolesports.com/live/lco/lco",
    "https://lolesports.com/live/cblol_academy":"https://lolesports.com/live/cblol_academy/cblol",
    "https://lolesports.com/live/cblol":"https://lolesports.com/live/cblol/cblol",
    "https://lolesports.com/live/lla":"https://lolesports.com/live/lla/lla",
    "https://lolesports.com/live/ljl-japan/ljl":"https://lolesports.com/live/ljl-japan/riotgamesjp",
    "https://lolesports.com/live/ljl-japan":"https://lolesports.com/live/ljl-japan/riotgamesjp",
    "https://lolesports.com/live/turkiye-sampiyonluk-ligi":"https://lolesports.com/live/turkiye-sampiyonluk-ligi/riotgamesturkish",
    "https://lolesports.com/live/cblol-brazil":"https://lolesports.com/live/cblol-brazil/cblol",
    "https://lolesports.com/live/pcs/lXLbvl3T_lc":"https://lolesports.com/live/pcs/lolpacific",
    "https://lolesports.com/live/ljl_academy/ljl":"https://lolesports.com/live/ljl_academy/riotgamesjp",
    "https://lolesports.com/live/european-masters":"https://lolesports.com/live/european-masters/EUMasters",
    "https://lolesports.com/live/worlds":"https://lolesports.com/live/worlds/riotgames",
}    

###################################################

parser = argparse.ArgumentParser(prog='CapsuleFarmer.exe', description='Farm Esports Capsules by watching lolesports.com.')
parser.add_argument('-b', '--browser', dest="browser", choices=['chrome', 'firefox', 'edge'], default="chrome",
                    help='Select one of the supported browsers')
parser.add_argument('-c', '--config', dest="configPath", default="./config.yaml",
                    help='Path to a custom config file')
parser.add_argument('-d', '--delay', dest="delay", default=600, type=int,
                    help='Time spent sleeping between match checking (in seconds)')
args = parser.parse_args()

print("*********************************************************")
print("*          Thank you for using Capsule Farmer!          *")
print("* Please consider supporting League of Poro on YouTube. *")
print("*********************************************************")
print()

# Mutes preexisting loggers like selenium_driver_updater
log = Logger().createLogger()

hasAutoLogin = False
isHeadless = False
username = "NoUsernameInConfig" # None
password = "NoPasswordInConfig" # None
browser = args.browser
delay = args.delay
try:
    config = readConfig(args.configPath)
    log.info(f"Using configuration from: {args.configPath}")
    if "autologin" in config and config["autologin"]["enable"]:
        username = config["autologin"]["username"]
        password = config["autologin"]["password"]
        hasAutoLogin = True
    if "headless" in config:
        isHeadless = config["headless"]
    if "browser" in config and config["browser"] in ['chrome', 'firefox', 'edge']:
        browser = config["browser"]
    if "delay" in config:
        delay = int(config["delay"])
except FileNotFoundError:
    log.warning("Configuration file not found. IGNORING...")
except (yaml.scanner.ScannerError, yaml.parser.ParserError) as e:
    log.warning("Invalid configuration file. IGNORING...")
except KeyError:
    log.warning("Configuration file is missing mandatory entries. Using default values instead...")

if not (isHeadless and hasAutoLogin):
    log.info("Consider using the headless mode for improved performance and stability.")

try:
    webdriver = Webdriver(browser=browser, headless=isHeadless and hasAutoLogin)
    driver = webdriver.createWebdriver()
except Exception as ex:
    print(ex)
    print("CANNOT CREATE A WEBDRIVER!\nPress any key to exit...")
    input()
    exit()

driver.get("https://lolesports.com/schedule")

login = Login(log=log, driver=driver)
rewards = Rewards(log=log, driver=driver)
match = Match(driver=driver)
twitch = Twitch(driver=driver)

if hasAutoLogin:
    try:
        login.logIn(username, password)
    except TimeoutException:
        log.error("Automatic login failed, incorrect credentials?")
        if isHeadless:
            driver.quit()
            log.info("Exiting...")
            exit()

while not driver.find_elements(by=By.CSS_SELECTOR, value="div.riotbar-summoner-name"):
    if not hasAutoLogin:
        log.info("Waiting for login")
    else: 
        log.info("Please log in manually")
    time.sleep(5)
log.info("Okay, we're in")

currentWindows = {}
originalWindow = driver.current_window_handle

while True:
    driver.switch_to.window(originalWindow) # just to be sure
    time.sleep(2)
    driver.get("https://lolesports.com/schedule")
    time.sleep(5)
    liveMatches = match.getLiveMatches()
    if len(liveMatches) == 1:
        log.info(f"There is 1 match live")
    else:
        log.info(f"There are {len(liveMatches)} matches live")

    # Close windows finished matches
    toRemove = []
    for k in currentWindows.keys():
        driver.switch_to.window(currentWindows[k])
        if k not in liveMatches:
            log.info(f"{k} has finished")
            driver.close()
            toRemove.append(k)
            driver.switch_to.window(originalWindow)
            time.sleep(5)
        else:
            rewards.checkRewards(k)
    for k in toRemove:
        currentWindows.pop(k, None)
    driver.switch_to.window(originalWindow)  

    # Open new live matches
    newLiveMatches = set(liveMatches) - set(currentWindows.keys())
    for match in newLiveMatches:
        driver.switch_to.new_window('tab')
        time.sleep(2)
        currentWindows[match] = driver.current_window_handle
        if match in OVERRIDES:
            url = OVERRIDES[match]
            log.info(f"Overriding {match} to {url}")
        else:
            url = match
        driver.get(url)
        rewards.checkRewards(url)
        try:
            twitch.setTwitchQuality()
            log.info("Twitch quality set successfully")
        except TimeoutException:
            log.warning(f"Cannot set the Twitch player quality. Is the match on Twitch?")
        time.sleep(5)

    driver.switch_to.window(originalWindow)
    log.info(f"Next check: {datetime.now() + timedelta(seconds=delay)}")
    time.sleep(delay)

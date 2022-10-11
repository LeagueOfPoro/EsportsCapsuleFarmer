from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
import argparse
from EsportsCapsuleFarmer.Overrides import Overrides

# Classes
from EsportsCapsuleFarmer.Setup.LoginHandler import LoginHandler
from EsportsCapsuleFarmer.Setup.VersionManager import VersionManager
from EsportsCapsuleFarmer.Setup.Webdriver import Webdriver
from EsportsCapsuleFarmer.Setup.Logger.Logger import Logger
from EsportsCapsuleFarmer.Setup.Config import Config

from EsportsCapsuleFarmer.Match import Match

###################################################

CURRENT_VERSION = 3.6

parser = argparse.ArgumentParser(prog='CapsuleFarmer.exe', description='Farm Esports Capsules by watching lolesports.com.')
parser.add_argument('-b', '--browser', dest="browser", choices=['chrome', 'firefox', 'edge'], default="chrome",
                    help='Select one of the supported browsers')
parser.add_argument('-c', '--config', dest="configPath", default="./config.yaml",
                    help='Path to a custom config file')
parser.add_argument('-d', '--delay', dest="delay", default=600, type=int,
                    help='Time spent sleeping between match checking (in seconds)')
args = parser.parse_args()

print("*********************************************************")
print(f"*        Thank you for using Capsule Farmer v{CURRENT_VERSION}!       *")
print("* Please consider supporting League of Poro on YouTube. *")
print("*********************************************************")
print()

# Mutes preexisting loggers like selenium_driver_updater
log = Logger().createLogger()
config = Config(log=log, args=args).readConfig()
hasAutoLogin, isHeadless, username, password, browser, delay, customOverrides = config.getArgs()
overrides = Overrides(customOverrides)

if not VersionManager.isLatestVersion(CURRENT_VERSION):
    log.warning("NEW VERSION AVAILABLE!!! Download it from: https://github.com/LeagueOfPoro/EsportsCapsuleFarmer/releases/latest")

try:
    driver = Webdriver(browser=browser, headless=isHeadless and hasAutoLogin).createWebdriver()
except Exception as ex:
    print(ex)
    print("CANNOT CREATE A WEBDRIVER! Are you running the latest browser?\nPress any key to exit...")
    input()
    exit()

loginHandler = LoginHandler(log=log, driver=driver)

driver.get("https://lolesports.com/schedule")

# Handle login
if hasAutoLogin:
    try:
        loginHandler.automaticLogIn(username, password)
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
        log.warning("Please log in manually")
    time.sleep(5)
log.debug("Okay, we're in")

Match(log=log, driver=driver, overrides=overrides).watchForMatches(delay=delay)

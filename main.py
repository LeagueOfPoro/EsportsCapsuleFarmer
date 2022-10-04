from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
import argparse

# Classes
from Classes.Setup.LoginHandler import LoginHandler
from Classes.Setup.Webdriver import Webdriver
from Classes.Setup.Logger.Logger import Logger
from Classes.Setup.Config import Config

from Classes.EsportCapsuleFarmer.Match import Match

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
config = Config(log=log, args=args).readConfig()
hasAutoLogin, isHeadless, username, password, browser, delay = config.getArgs()

try:
    driver = Webdriver(browser=browser, headless=isHeadless and hasAutoLogin).createWebdriver()
except Exception as ex:
    print(ex)
    print("CANNOT CREATE A WEBDRIVER!\nPress any key to exit...")
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

Match(log=log, driver=driver).watchForMatches(delay=delay)

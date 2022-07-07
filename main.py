import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
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
    "https://lolesports.com/live/lcs":"https://lolesports.com/live/lcs/lcs",
    "https://lolesports.com/live/cblol_academy":"https://lolesports.com/live/cblol_academy/cblol"
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

def logIn(driver, username, password):
    driver.get("https://lolesports.com/")
    time.sleep(2)
    els = driver.find_elements(by=By.CSS_SELECTOR, value="a[data-riotbar-link-id=login]")
    for el in els:
        try:
            el.click()
        except:
            continue 
    wait = WebDriverWait(driver, 10)
    usernameInput = wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, "input[name=username]")))
    usernameInput.send_keys(username)
    passwordInput = wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, "input[name=password]")))
    passwordInput.send_keys(password)
    submitButton = wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, "button[type=submit]")))
    submitButton.click()

    # wait until the login process finishes
    wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, "div.riotbar-summoner-name"))) 


###################################################
log = logging.getLogger("League of Poro")
log.setLevel('DEBUG')
chromedriver_autoinstaller.install()

hasValidConfig = False
hasAutoLogin = False
username = "NoUsernameInConfig" # None
password = "NoPasswordInConfig" #  None
try:
    config = readConfig(CONFIG_LOCATION)
    hasValidConfig = True
    if "autologin" in config:
        if config["autologin"]["enable"]:
            username = config["autologin"]["username"]
            password = config["autologin"]["password"]
            hasAutoLogin = True
except FileNotFoundError:
    log.warning("Configuration file not found. IGNORING...")
except (yaml.scanner.ScannerError, yaml.parser.ParserError) as e:
    log.warning("Invalid configuration file. IGNORING...")
except KeyError:
    log.warning("Configuration file is missing mandatory entries. Using default values instead...")

options = webdriver.ChromeOptions() 
options.add_argument('log-level=3')
driver = webdriver.Chrome(options=options)
driver.get("https://lolesports.com/")
time.sleep(2)

if hasAutoLogin:
    logIn(driver, username, password)

while not driver.find_elements(by=By.CSS_SELECTOR, value="div.riotbar-summoner-name"):
    if not hasAutoLogin:
        log.info("Waiting for log in")
    else: 
        log.info("Automatic login failed, please log in manually")
    time.sleep(5)
log.info("Okay, we're in")
time.sleep(5)

currentWindows = {}
originalWindow = driver.current_window_handle

while True:
    driver.switch_to.window(originalWindow) # just to be sure
    time.sleep(5)
    driver.get("https://lolesports.com/")
    time.sleep(15)
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




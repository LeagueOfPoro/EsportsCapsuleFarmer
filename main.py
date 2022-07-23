import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium_driver_updater import DriverUpdater
import time
import yaml
import argparse

# Force Twitch player
OVERRIDDES = {
    "https://lolesports.com/live/lck_challengers_league":"https://lolesports.com/live/lck_challengers_league/lckcl",
    "https://lolesports.com/live/lpl":"https://lolesports.com/live/lpl/lpl",
    "https://lolesports.com/live/lck":"https://lolesports.com/live/lck/lck",
    "https://lolesports.com/live/lec":"https://lolesports.com/live/lec/lec",
    "https://lolesports.com/live/lcs":"https://lolesports.com/live/lcs/lcs",
    "https://lolesports.com/live/lco":"https://lolesports.com/live/lco/lco",
    "https://lolesports.com/live/cblol_academy":"https://lolesports.com/live/cblol_academy/cblol",
    "https://lolesports.com/live/cblol":"https://lolesports.com/live/cblol/cblol",
    "https://lolesports.com/live/lla":"https://lolesports.com/live/lla/lla"
}

def createWebdriver(browser, headless):
    match browser:
        case "chrome":
            driverPath = DriverUpdater.install(path=".", driver_name=DriverUpdater.chromedriver, upgrade=True, check_driver_is_up_to_date=True, old_return=False)
            options = addWebdriverOptions(webdriver.ChromeOptions() , headless)
            service = ChromeService(driverPath)
            return webdriver.Chrome(service=service, options=options)            
        case "firefox":
            driverPath = DriverUpdater.install(path=".", driver_name=DriverUpdater.geckodriver, upgrade=True, check_driver_is_up_to_date=True, old_return=False)
            options = addWebdriverOptions(webdriver.FirefoxOptions() , headless)
            service = FirefoxService(driverPath)
            return webdriver.Firefox(service=service, options=options)
        case "edge":  # NO CURRENT DRIVER AVAILABLE
            driverPath = DriverUpdater.install(path=".", driver_name=DriverUpdater.edgedriver, upgrade=True, check_driver_is_up_to_date=True, old_return=False)
            options = addWebdriverOptions(webdriver.EdgeOptions() , headless)
            service = EdgeService(driverPath)
            return webdriver.Edge(service=service, options=options)

def addWebdriverOptions(options, headless):
    options.add_argument("--log-level=3")
    if headless:
        options.add_argument("--headless")
    return options

def getLiveMatches(driver):
    matches = []
    elements = driver.find_elements(by=By.CSS_SELECTOR, value=".live.event")
    for element in elements:
        matches.append(element.get_attribute("href"))
    return matches

def readConfig(filepath):
    with open(filepath, "r") as f:
        return yaml.safe_load(f)

def logIn(driver, username, password):
    driver.get("https://lolesports.com/schedule")
    time.sleep(2)

    log.info("Moving to log in page")
    el = driver.find_element(by=By.CSS_SELECTOR, value="a[data-riotbar-link-id=login]")
    driver.execute_script("arguments[0].click();", el)

    log.info("Logging in")

    wait = WebDriverWait(driver, 20)
    usernameInput = wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, "input[name=username]")))
    usernameInput.send_keys(username)
    passwordInput = wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, "input[name=password]")))
    passwordInput.send_keys(password)
    submitButton = wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, "button[type=submit]")))
    driver.execute_script("arguments[0].click();", submitButton)
    
    log.info("Credentials submited")
    # wait until the login process finishes
    wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, "div.riotbar-summoner-name")))


def setTwitchQuality(driver):
    wait = WebDriverWait(driver, 10)
    wait.until(ec.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe[title=Twitch]")))
    settingsButton = wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, "button[data-a-target=player-settings-button]")))
    driver.execute_script("arguments[0].click();", settingsButton)
    qualityButton = wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, "button[data-a-target=player-settings-menu-item-quality]")))
    driver.execute_script("arguments[0].click();", qualityButton)
    options = wait.until(ec.presence_of_all_elements_located((By.CSS_SELECTOR, "input[data-a-target=tw-radio]")))
    driver.execute_script("arguments[0].click();", options[-1])

###################################################

parser = argparse.ArgumentParser(prog='CapsuleFarmer.exe', description='Farm Esports Capsules by watching lolesports.com.')
parser.add_argument('-b', '--browser', dest="browser", choices=['chrome', 'firefox', 'edge'], default="chrome",
                    help='Select one of the supported browsers')
parser.add_argument('-c', '--config', dest="configPath", default="./config.yaml",
                    help='Path to a custom config file')
args = parser.parse_args()

print("*********************************************************")
print("*          Thank you for using Capsule Farmer!          *")
print("* Please consider supporting League of Poro on YouTube. *")
print("*********************************************************")
print()

log = logging.getLogger("League of Poro")
log.setLevel('DEBUG')
ch = logging.StreamHandler()
ch.setLevel('DEBUG')
formatter = logging.Formatter('%(levelname)s: %(asctime)s - %(message)s', '%Y/%m/%d %H:%M:%S')
ch.setFormatter(formatter)
log.addHandler(ch)

hasAutoLogin = False
isHeadless = False
username = "NoUsernameInConfig" # None
password = "NoPasswordInConfig" # None
try:
    config = readConfig(args.configPath)
    log.info(f"Using configuration from: {args.configPath}")
    if "autologin" in config:
        if config["autologin"]["enable"]:
            username = config["autologin"]["username"]
            password = config["autologin"]["password"]
            hasAutoLogin = True
    if "headless" in config:
        isHeadless = config["headless"]
except FileNotFoundError:
    log.warning("Configuration file not found. IGNORING...")
except (yaml.scanner.ScannerError, yaml.parser.ParserError) as e:
    log.warning("Invalid configuration file. IGNORING...")
except KeyError:
    log.warning("Configuration file is missing mandatory entries. Using default values instead...")

if not (isHeadless and hasAutoLogin):
    log.info("Consider using the headless mode for improved performance and stability.")
driver = createWebdriver(args.browser, isHeadless and hasAutoLogin)

driver.get("https://lolesports.com/schedule")

if hasAutoLogin:
    try:
        logIn(driver, username, password)
    except TimeoutException:
        log.error("Automatic login failed, incorrect credentials?")
        if isHeadless:
            driver.quit()
            log.info("Exitting...")
            exit()

while not driver.find_elements(by=By.CSS_SELECTOR, value="div.riotbar-summoner-name"):
    if not hasAutoLogin:
        log.info("Waiting for log in")
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
        time.sleep(5)
        try:
            setTwitchQuality(driver)
            log.info("Twitch quality set successfully")
        except:
            log.warning(f"Cannot set the Twitch player quality. Is the match on Twitch?")
        time.sleep(30)

    driver.switch_to.window(originalWindow)
    time.sleep(600)

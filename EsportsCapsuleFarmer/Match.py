from selenium.webdriver.common.by import By
import time
from datetime import datetime, timedelta
from selenium.common.exceptions import TimeoutException

from EsportsCapsuleFarmer.Rewards import Rewards
from EsportsCapsuleFarmer.Providers.Twitch import Twitch

class Match:

    def __init__(self, log, driver, overrides) -> None:
        self.log = log
        self.driver = driver
        self.rewards = Rewards(log=log, driver=driver)
        self.twitch = Twitch(driver=driver)
        self.overrides = overrides

        self.currentWindows = {}
        self.originalWindow = self.driver.current_window_handle

    def watchForMatches(self, delay):
        self.currentWindows = {}
        self.originalWindow = self.driver.current_window_handle

        while True:
            self.driver.switch_to.window(self.originalWindow) # just to be sure
            time.sleep(2)
            self.driver.get("https://lolesports.com/schedule")
            time.sleep(5)
            liveMatches = self.getLiveMatches()
            if len(liveMatches) == 1:
                self.log.info(f"There is 1 match live")
            else:
                self.log.info(f"There are {len(liveMatches)} matches live")

            self.closeFinishedMatches(liveMatches=liveMatches)
            self.openNewMatches(liveMatches=liveMatches)

            self.driver.switch_to.window(self.originalWindow)
            self.log.info(f"Next check: {datetime.now() + timedelta(seconds=delay)}")
            time.sleep(delay)

    def getLiveMatches(self):
        """
        Fetches all the current/live esports matches on the LoL Esports website.
        """
        matches = []
        elements = self.driver.find_elements(by=By.CSS_SELECTOR, value=".live.event")
        for element in elements:
            matches.append(element.get_attribute("href"))
        return matches

    def closeFinishedMatches(self, liveMatches):
        toRemove = []
        for k in self.currentWindows.keys():
            self.driver.switch_to.window(self.currentWindows[k])
            if k not in liveMatches:
                self.log.info(f"{k} has finished")
                self.driver.close()
                toRemove.append(k)
                self.driver.switch_to.window(self.originalWindow)
                time.sleep(5)
            else:
                self.rewards.checkRewards(k)
        for k in toRemove:
            self.currentWindows.pop(k, None)
        self.driver.switch_to.window(self.originalWindow)  

    def openNewMatches(self, liveMatches):
        newLiveMatches = set(liveMatches) - set(self.currentWindows.keys())
        for match in newLiveMatches:
            self.driver.switch_to.new_window('tab')
            time.sleep(2)
            self.currentWindows[match] = self.driver.current_window_handle
            override = self.overrides.getOverride(match)
            if override:
                url = override
                self.log.info(f"Overriding {match} to {url}")
            else:
                url = match
            self.driver.get(url)
            self.rewards.checkRewards(url)
            try:
                self.twitch.setTwitchQuality()
                self.log.debug("Twitch quality set successfully")
            except TimeoutException:
                self.log.critical(f"Cannot set the Twitch player quality. Is the match on Twitch?")
            time.sleep(5)

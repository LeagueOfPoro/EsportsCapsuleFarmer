from selenium.webdriver.common.by import By
import time
from datetime import datetime, timedelta
from selenium.common.exceptions import TimeoutException

from EsportsCapsuleFarmer.Rewards import Rewards
from EsportsCapsuleFarmer.Providers.Twitch import Twitch

class Match:
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

    def __init__(self, log, driver) -> None:
        self.log = log
        self.driver = driver
        self.rewards = Rewards(log=log, driver=driver)
        self.twitch = Twitch(driver=driver)

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
            if match in self.OVERRIDES:
                url = self.OVERRIDES[match]
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

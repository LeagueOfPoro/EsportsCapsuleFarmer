from selenium.webdriver.common.by import By

class Match:
    def __init__(self, driver) -> None:
        self.driver = driver


    def getLiveMatches(self):
        """
        Fetches all the current/live esports matches on the LoL Esports website.
        """
        matches = []
        elements = self.driver.find_elements(by=By.CSS_SELECTOR, value=".live.event")
        for element in elements:
            matches.append(element.get_attribute("href"))
        return matches

import requests as req

class Overrides:
    def __init__(self, log, customOverrides = {}) -> None:
        self.customOverrides = customOverrides
        self.downloadedOverrides = {}
        self.downloadOverrides()
    
    def downloadOverrides(self):
        overridesResponse = req.get("https://raw.githubusercontent.com/LeagueOfPoro/EsportsCapsuleFarmer/overrides/overrides.json", headers={'Cache-Control': 'no-cache'})
        self.downloadedOverrides = overridesResponse.json()
    
    def getOverride(self, url):
        override = self.customOverrides.get(url, '')
        if not override:
            override = self.downloadedOverrides.get(url, '')
        return override
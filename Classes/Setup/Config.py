import yaml

class Config():
    def __init__(self, log, args) -> None:
        self.log = log
        self.args = args
        self.hasAutoLogin = False
        self.isHeadless = False
        self.username = "NoUsernameInConfig" # None
        self.password = "NoPasswordInConfig" # None
        self.browser = args.browser
        self.delay = args.delay

    def getArgs(self):
        return self.hasAutoLogin, self.isHeadless, self.username, self.password, self.browser, self.delay

    def openConfigFile(self, filepath):
        with open(filepath, "r",  encoding='utf-8') as f:
            return yaml.safe_load(f)

    def readConfig(self):
        try:
            config = self.openConfigFile(self.args.configPath)
            self.log.info(f"Using configuration from: {self.args.configPath}")
            if "autologin" in config and config["autologin"]["enable"]:
                self.username = config["autologin"]["username"]
                self.password = config["autologin"]["password"]
                self.hasAutoLogin = True
            if "headless" in config:
                self.isHeadless = config["headless"]
            if "browser" in config and config["browser"] in ['chrome', 'firefox', 'edge']:
                self.browser = config["browser"]
            if "delay" in config:
                self.delay = int(config["delay"])
        except FileNotFoundError:
            self.log.warning("Configuration file not found. IGNORING...")
        except (yaml.scanner.ScannerError, yaml.parser.ParserError) as e:
            self.log.warning("Invalid configuration file. IGNORING...")
        except KeyError:
            self.log.warning("Configuration file is missing mandatory entries. Using default values instead...")

        if not (self.isHeadless and self.hasAutoLogin):
            self.log.info("Consider using the headless mode for improved performance and stability.")

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

class LoginHandler: 
    def __init__(self, log, driver) -> None:
        self.log = log
        self.driver = driver

    def automaticLogIn(self, username, password):
        """
        Automatically logs into the user's account on the LoL Esports website.
        """
        self.driver.get("https://lolesports.com/schedule")
        time.sleep(2)

        self.log.info("Moving to login page")
        el = self.driver.find_element(by=By.CSS_SELECTOR, value="a[data-riotbar-link-id=login]")
        self.driver.execute_script("arguments[0].click();", el)

        self.log.info("Logging in")

        wait = WebDriverWait(self.driver, 20)
        usernameInput = wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, "input[name=username]")))
        usernameInput.send_keys(username)
        passwordInput = wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, "input[name=password]")))
        passwordInput.send_keys(password)
        submitButton = wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, "button[type=submit]")))
        self.driver.execute_script("arguments[0].click();", submitButton)
        self.log.info("Credentials submitted")

        # check for 2FA
        time.sleep(5)
        if len(self.driver.find_elements(by=By.CSS_SELECTOR, value="div.text__web-code")) > 0:
            self.insertTwoFactorCode(self.driver)

        # wait until the login process finishes
        wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, "div.riotbar-summoner-name")))

    def insertTwoFactorCode(self):
        wait = WebDriverWait(self.driver, 20)
        authText = wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, "h5.grid-panel__subtitle")))
        self.log.info(f'Enter 2FA code ({authText.text})')
        code = input('Code: ')
        codeInput = wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, "div.codefield__code--empty > div > input")))
        codeInput.send_keys(code)

        submitButton = wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, "button[type=submit]")))
        self.driver.execute_script("arguments[0].click();", submitButton)
        self.log.info("Code submitted")

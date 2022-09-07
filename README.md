# League of Poro's Esports Capsule Farmer

Are you tired of watching professional League of Legends games? Do you watch only for the drops?

This tool makes the Chrome browser watch the matches for you!

### Features
- Checks for new live matches
- Closes finished matches
- Automatically logs user in
- Runs in background
- Multiple accounts
- Sets Twitch quality to the lowest possible
- Checks for the Rewards check mark
- Experimental support for Firefox and Edge

### Video Tutorial

_(Outdated, will be updated in the future)_

[![Tutorial](https://img.youtube.com/vi/FCk6MoSjt5w/0.jpg)](https://www.youtube.com/watch?v=FCk6MoSjt5w)

[![Total alerts](https://img.shields.io/lgtm/alerts/g/LeagueOfPoro/EsportsCapsuleFarmer.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/LeagueOfPoro/EsportsCapsuleFarmer/alerts/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/LeagueOfPoro/EsportsCapsuleFarmer.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/LeagueOfPoro/EsportsCapsuleFarmer/context:python)

## Installation (simple)

**⚠️ This project utilizes the [Google Chrome browser](https://www.google.com/chrome/) by default. However, there's an experimental support for Firefox and Edge (see [Configuration](#configuration) or [CLI](#cli) if you want to use alternative browsers). Please make sure you have the selected browser installed!**

1. Download and run the latest CapsuleFarmer.zip from [Releases tab](https://github.com/LeagueOfPoro/EsportsCapsuleFarmer/releases)
2. Extract the archive
3. (Optional) Edit the configuration file with a text editor (e.g. Notepad) - see [Configuration](#configuration) for details
4. Run `CapsuleFarmer.exe`
5. If you do not use the autologin feature - log into your account 

_Note: I am using Google Chrome + automatic login + headless. This will be the most stable and preferred configuration._

## Configuration

**⚠️ The configuration file ([config.yaml](config.yaml)) MUST be present in the SAME folder as the executable! To use non-default path, see [CLI](#cli).**

**⚠️ Automatic login will not work with 2FA enabled.**

Default configuration:
```yaml
headless: false
autologin:
  enable: false
```

If you wish to enable automatic login and to run the browser in the background:
```yaml
headless: true
autologin:
  enable: true
  username: "YourUsername"
  password: "YourPassword"
```

Experimental support for alternative browsers (default: _chrome_):
```yaml
browser: firefox # Other options: chrome, edge
```

Set delay in seconds between checks for new matches (default: _600_):
```yaml
delay: 600
```

## Multiple accounts

The program supports multiple accounts by default. However, if you want to use the automatic login + headless mode, the best method to start the program is to use the included [batch script](combine.bat).

**⚠️ Run the CapsuleFarmer.exe at least once before you attempt to use multiple accounts. Otherwise every instance will try to download the WebDriver and bad things WILL happen.**

1. Create configuration file for each account
2. Open the example [combine.bat](combine.bat) in a text editor
3. For each account, add path to the account's config file, e.g. `START CapsuleFarmer.exe -c config.account1.yaml`
4. Run the _.bat_ script

## Common Errors/Issues

- *The Riot Account login page is not loading*
    - Simply refresh the page a bunch of times. This is an issue with the website, not the program.
- *There are warnings / errors but the program runs fine* 
    - You can ignore them. These are most of the time Chrome related warnings and errors. As long as the program runs fine, you can ignore them.
- *Program crashes immediately*
  ```
  Traceback (most recent call last):
  File "main.py", line 73, in <module>
  File "chromedriver_autoinstaller\__init__.py", line 20, in install
  File "chromedriver_autoinstaller\utils.py", line 195, in download_chromedriver
  File "chromedriver_autoinstaller\utils.py", line 118, in get_chrome_version
  IndexError: list index out of range
  [7016] Failed to execute script 'main' due to unhandled exception!
  ```
    - You don't have Google Chrome installed.
- *It doesn't work*
    - [Have you tried turning it off and on again?](https://www.youtube.com/watch?v=p85xwZ_OLX0)

## CLI
```bash
usage: CapsuleFarmer.exe [-h] [-b {chrome,firefox,edge}] [-c CONFIGPATH] [-d DELAY]

Farm Esports Capsules by watching lolesports.com.

options:
  -h, --help            show this help message and exit
  -b {chrome,firefox,edge}, --browser {chrome,firefox,edge}
                        Select one of the supported browsers
  -c CONFIGPATH, --config CONFIGPATH
                        Path to a custom config file
  -d DELAY, --delay DELAY
                        Time spent sleeping between match checking (in seconds)
```

## Installation (advanced)

### Prerequisities
- Python >= 3.10.1
- pipenv (`pip install pipenv`)

### Step by step
1. Clone this repo - `git clone https://github.com/LeagueOfPoro/EsportsCapsuleFarmer.git`
2. Move to the directory -  `cd EsportsCapsuleFarmer`
3. Install the Python virtual environment - `pipenv install`
4. (Optional) Edit the configuration file
5. Run the tool - `pipenv run python ./main.py`

### Create EXE
1.  `pipenv install --dev`
2.  `pipenv run pyinstaller -F --icon=poro.ico ./main.py`

## Forks
[Dockerized version for Raspbery Pi](https://github.com/kacperkr90/EsportsCapsuleFarmer) by [kacperkr90](https://github.com/kacperkr90)

## Support my work
<a href='https://www.youtube.com/channel/UCwgpdTScSd788qILhLnyyyw/join' target='_blank'><img height='35' style='border:0px;height:46px;' src='https://share.leagueofporo.com/yt_member.png' border='0' alt='Become a channel member on YouTube' />

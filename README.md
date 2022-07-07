# League of Poro's Esports Capsule Farmer

Are you tired of watching professional League of Legends games? Do you watch only for the drops?

This tool makes the Chrome browser watch the matches for you!

### Features
- Checks for new live matches
- Closes finished matches
- Automatically logs user in
- Runs in background
- Sets Twitch quality to lowest possible

### Video Tutorial
[![Tutorial](https://img.youtube.com/vi/FCk6MoSjt5w/0.jpg)](https://www.youtube.com/watch?v=FCk6MoSjt5w)

[![Total alerts](https://img.shields.io/lgtm/alerts/g/LeagueOfPoro/EsportsCapsuleFarmer.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/LeagueOfPoro/EsportsCapsuleFarmer/alerts/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/LeagueOfPoro/EsportsCapsuleFarmer.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/LeagueOfPoro/EsportsCapsuleFarmer/context:python)


# Installation

### Requirements
⚠️ This project utilizes the [Google Chrome browser](https://www.google.com/chrome/). Please ensure you have it installed before attempting to build or run the project.

Download and run the latest `CapsuleFarmer.exe` from the [Releases tab](/releases). 
Alternatively, you can build the project your self following the instructions [here](#compile-the-program-your-self)

# Configuration
**The configuration file ([config.yaml](config.yaml)) MUST be present in the SAME folder as the executable!**

Default configuration:
```yaml
version: 1.1

headless: false
autologin:
  enable: false
```

If you wish to enable automatic login and to run the browser in the background:
```yaml
version: 1.1

headless: true
autologin:
  enable: true
  username: YourUsername
  password: YourPassword
```

# How to use
1. Download and run the latest CapsuleFarmer.zip from [Releases tab](/releases)
2. Extract the archive
3. (Optional) Edit the configuration file with a text editor (e.g. Notepad/[Notepad++](https://notepad-plus-plus.org/downloads/)) - see [Configuration](#configuration) for details
4. Run `CapsuleFarmer.exe` 

# Common Errors/Issues

### - The Riot Account login page is not loading
Simply refresh the page a bunch of times. This is an issue with the website, not the program. 
### - There are warnings / errors but the program runs fine 
You can ignore them. These are most of the time Chrome related warnings and errors. As long as the program runs fine, you can ignore them.

# Compile the program your self

### Prerequisities
- Python 3.10
- pipenv (`pip install pipenv`)

### Step by step
1. Clone this repo - `git clone https://github.com/LeagueOfPoro/EsportsCapsuleFarmer.git`
2. Move to the directory -  `cd EsportsCapsuleFarmer`
3. Install the Python virtual environment - `pipenv install`
4. Run the tool - `pipenv run python .\main.py`

### Create EXE
1.  `pipenv install --dev`
2.  `pipenv run pyinstaller -F --icon=poro.ico .\main.py`


# Future features
Force the video player to use Twitch (in progress)

# Support my work
<a href='https://www.youtube.com/channel/UCwgpdTScSd788qILhLnyyyw/join' target='_blank'><img height='35' style='border:0px;height:46px;' src='https://share.leagueofporo.com/yt_member.png' border='0' alt='Become a channel member on YouTube' />

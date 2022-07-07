# League of Poro's Esports Capsule Farmer

Are you tired of watching professional League of Legends games? Do you watch only for the drops?

This tool makes the Chrome browser watch the matches for you!

### Tutorial
[![Tutorial](https://img.youtube.com/vi/FCk6MoSjt5w/0.jpg)](https://www.youtube.com/watch?v=FCk6MoSjt5w)

## Features
- Checks for new live matches
- Closes finished matches
- Automatically logs user in
- Runs in background

## Requirements
- [Chrome browser](https://www.google.com/chrome/)

## How to use
1. Start the program
2. Wait for the browser to load
3. Log in
4. Sit back and relax

## Configuration
**The configuration file ([config.yaml](config.yaml)) must be present in the same folder as the executable!**

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

## Installation (simple)
1. Download and run the latest CapsuleFarmer.zip from [Releases tab](https://github.com/LeagueOfPoro/EsportsCapsuleFarmer/releases)
2. Extract the archive
3. (Optional) Edit the configuration file with a text editor (e.g. Notepad) - see [Configuration](#configuration) for details
4. Run `CapsuleFarmer.exe` 

## Installation (advanced)

### Prerequisities
- Python 3.10
- pipenv (`pip install pipenv`)

### Step by step
1. Clone this repo - `git clone https://github.com/LeagueOfPoro/EsportsCapsuleFarmer.git`
2. Move to the directory -  `cd EsportsCapsuleFarmer`
3. Install the Python virtual environment - `pipenv install`
4. (Optional) Edit the configuration file
5. Run the tool - `pipenv run python .\main.py`

### Create EXE
1.  `pipenv install --dev`
2.  `pipenv run pyinstaller -F --icon=poro.ico .\main.py`


## Future features
- Force the video player to use Twitch (in progress)

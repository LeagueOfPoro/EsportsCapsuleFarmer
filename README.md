# League of Poro's Esports Capsule Farmer

Are you tired of watching professional League of Legends games? Do you watch only for the drops?

This tool makes the Chrome browser watch the matches for you!

### Tutorial
[![Tutorial](https://img.youtube.com/vi/FCk6MoSjt5w/0.jpg)](https://www.youtube.com/watch?v=FCk6MoSjt5w)

## Features
- Checks for new live matches
- Closes finished matches

## Requirements
- [Chrome browser](https://www.google.com/chrome/)

## How to use
1. Start the program
2. Wait for the browser to load
3. Log in
4. Sit back and relax

## Installation (simple)
Download and run the latest CapsuleFarmer.exe from [Releases tab](https://github.com/LeagueOfPoro/EsportsCapsuleFarmer/releases).

## Installation (advanced)

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


## Future features
- Force the video player to use Twitch (in progress)
- Automatic log in
- Headless browser (if possible)

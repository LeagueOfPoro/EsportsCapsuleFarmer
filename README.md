# League of Poro's Esports Capsule Farmer

Are you tired of watching professional League of Legends games? Do you watch only for the drops?

This tool makes the Chrome browser watch the matches for you!

### Features
- Checks for new live matches
- Closes finished matches

### Video Tutorial
[![Tutorial](https://img.youtube.com/vi/FCk6MoSjt5w/0.jpg)](https://www.youtube.com/watch?v=FCk6MoSjt5w)

[![Total alerts](https://img.shields.io/lgtm/alerts/g/LeagueOfPoro/EsportsCapsuleFarmer.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/LeagueOfPoro/EsportsCapsuleFarmer/alerts/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/LeagueOfPoro/EsportsCapsuleFarmer.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/LeagueOfPoro/EsportsCapsuleFarmer/context:python)

# Requirements
This project utilizes the [Google Chrome browser](https://www.google.com/chrome/). Please ensure you have it installed before attempting to build or run the project.

# Installation
Download and run the latest CapsuleFarmer.exe from the [Releases tab](https://github.com/LeagueOfPoro/EsportsCapsuleFarmer/releases). Alternatively, you can build the project your self following the instructions [here](https://github.com/LeagueOfPoro/EsportsCapsuleFarmer#compile-the-program-your-self)

# How to use
1. Start the program
2. Wait for the browser to load
3. Log in
4. Sit back and relax

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


## Future features
- Force the video player to use Twitch (in progress)
- Automatic log in
- Headless browser (if possible)

activity-logger
===============

Log what workspace you're on and the active window.  The `IDLE_THRESHOLD` is currently 90 seconds.  So if you are not typing or moving the mouse for 90 seconds it's considered idle.

# About
I have a lot of different workspaces.  Some are for specific clients I work for.  
I wanted an easy way to keep track of how much time I was really spending on all my contracts.
I didn't want to do a lot of work.  Clocking in & clocking out.
**If someone else was doing this to me I'd consider it spyware. So DON'T install 
it on someone else's account/login.**

# Installing needed programs
``` 
sudo apt-get install xprintidle wmctrl xdotool python-mako
sudo pip install -r requirements.txt
git submodule init
git submodule update
```

# Usage
Open a terminal and run `./activity-logger.py`

Name your workspaces different names, and it'll log what windows is open and for
how long.

This uses http://strapdownjs.com/ to generate the markdown.

From there you just http://localhost:5001 to view your stats.

# Configuring
There is not much to configure.  You'll need to create a file called
`config_local.py` in the same folder as `activity-logger`

Contents of `config_local.py`
```
import re

# Number of seconds before the system considers you idle.
IDLE_THRESHOLD = 120

# Turn on/off Flask debugging
DEBUG = False

# Number of seconds to sleep() between checks/logging.
TIME_BETWEEN_CHECKS = 10

# This uses a find, replace format
# The 1st value is the 'find' and the 2nd is the replace.
# If you just use a string it's case insensitive.
# It's important to note that this only changes the title, and not the command
# that is running.
REPLACE_RULES = [
    # Replace all gmail Inbox (#) titles with "Inbox - Gmail"
    (re.compile("Inbox \(\d+\) .* Gmail"), "Inbox - Gmail"),
    # If the phrase '(Private Browsing)' is in the window title ... hide it.
    ("(Private Browsing)", "--hidden--"),
    ("banking", "--hidden--"),
    ("my bank name", "--hidden--"),
    ("bitcoin", "--hidden--"),
    ("some random program", "--hidden--")
]
```

# Autostart
If you want to constantly run this in the background every time you log in I use
something like the following in a script.

Contents of `/home/erm/bin/autostart.sh`
```
#!/bin/sh
cd /home/erm/git/activity-logger
./activity-logger.py &> /dev/null &
```

With a desktop entry in `~/.config/autostart`

Contents of `~/.config/autostart/autostart-sh.desktop`
```
[Desktop Entry]
Name=Autostart
Comment=Autostart Erm's scripts
Exec=/home/erm/bin/autostart.sh
```

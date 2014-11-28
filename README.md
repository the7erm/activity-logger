activity-logger
===============

Log what workspace your on and the active window

# About
I have multiple clients, and I have each client on their own workspace.  I wanted
to know where my time was going automatically.

# How to use.
``` sudo apt-get install xprintidle wmctrl xdotool python-mako ```
Open a terminal and run `./activity-logger.py`

Name your workspaces different names, and it'll log what windows is open and for
how long.  Currently it generates daily reports every minute.

It uses http://strapdownjs.com/ to generate the markdown.



activity-logger
===============

Log what workspace you're on and the active window.

# About
I have multiple clients, and I have each client on their own workspace.  I wanted
to know where my time was going automatically.  **If someone else was doing this
to me I'd consider it spyware. So DON'T install it on someone else's account.**

# How to use.
``` 
sudo apt-get install xprintidle wmctrl xdotool python-mako 
```

Open a terminal and run `./activity-logger.py`

Name your workspaces different names, and it'll log what windows is open and for
how long.  Currently it generates daily reports every minute.

It uses http://strapdownjs.com/ to generate the markdown.


## Sample output of daily.html

Here's a sample of a daily html file that's automatically generated every minute in `reports/`.

# Daily Activity 2014-11-28

#### Workspace - Active

Workspace | Time
--------- | ----
Personal | 03:21:55
Programing | 01:40:20

#### Workspace & Hour - Active

Workspace | Hour | Time
--------- | ---- | ----
Personal | 03:00 | 00:44:45
Personal | 04:00 | 00:54:35
Personal | 05:00 | 00:57:15
Personal | 06:00 | 00:16:40
Personal | 07:00 | 00:19:50
Personal | 12:00 | 00:08:40
Programing | 12:00 | 00:19:00
Programing | 13:00 | 00:50:40
Personal | 14:00 | 00:00:10
Programing | 14:00 | 00:30:40

#### Workspace & Command

Workspace | Command | Time
--------- | ------- | ----
Personal | sublime_text | 01:11:10
Personal | terminator | 00:16:30
Personal | update-manager | 00:00:10
Personal | firefox | 01:53:10
Personal | None | 00:00:10
Personal | idle | 05:41:45
Personal | pidgin | 00:00:40
Personal | fmp-pg.py | 00:00:05
Programing | sublime_text | 01:04:00
Programing | gmusicbrowser | 00:00:10
Programing | terminator | 00:08:00
Programing | firefox | 00:27:50
Programing | idle | 00:03:50
Programing | xfwm4-workspace-settings | 00:00:20
Client 1 | None | 00:00:05
Client 2 | None | 00:00:05

#### Command

Command | Time
------- | ----
sublime_text | 02:15:10
gmusicbrowser | 00:00:10
terminator | 00:24:40
update-manager | 00:00:10
firefox | 02:21:00
None | 00:00:30
idle | 05:45:35
pidgin | 00:01:00
fmp-pg.py | 00:00:05
xfwm4-workspace-settings | 00:00:30

#### Workspace, Command and Title

Workspace | Command | Title | Time
--------- | ------- | ----- | ----
Personal | sublime_text | activity-logger • (activity-logger) - Sublime Text 2 | 00:04:10
Personal | sublime_text | untitled (activity-logger) - Sublime Text 2 | 00:00:20
Personal | sublime_text | ~/git/activity-logger/README.md (activity-logger) - Sublime Text 2 | 00:00:20
Personal | sublime_text | ~/git/activity-logger/activity-logger.py (activity-logger) - Sublime Text 2 | 00:23:55
Personal | sublime_text | ~/git/activity-logger/activity-logger.py • (activity-logger) - Sublime Text 2 | 00:14:00
Personal | sublime_text | ~/git/activity-logger/reports/test.html (activity-logger) - Sublime Text 2 | 00:00:15
Personal | sublime_text | ~/git/activity-logger/templates/base.html (activity-logger) - Sublime Text 2 | 00:04:35
Personal | sublime_text | ~/git/activity-logger/templates/base.html • (activity-logger) - Sublime Text 2 | 00:03:45
Personal | sublime_text | ~/git/activity-logger/templates/daily.html (activity-logger) - Sublime Text 2 | 00:09:35
Personal | sublime_text | ~/git/activity-logger/templates/daily.html • (activity-logger) - Sublime Text 2 | 00:09:55
Personal | sublime_text | ~/git/activity-logger/templates/strapdown.js (activity-logger) - Sublime Text 2 | 00:00:20

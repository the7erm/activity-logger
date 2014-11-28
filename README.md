activity-logger
===============

Log what workspace you're on and the active window.

# About
I have multiple clients, and I have each client on their own workspace.  I wanted
to know where my time was going automatically.

# How to use.
``` sudo apt-get install xprintidle wmctrl xdotool python-mako ```
Open a terminal and run `./activity-logger.py`

Name your workspaces different names, and it'll log what windows is open and for
how long.  Currently it generates daily reports every minute.

It uses http://strapdownjs.com/ to generate the markdown.


## Sample of daily.html

# Daily Activity 2014-11-28
#### By Desktop
Desktop | Time
------- | -----
Hacking | 00:00:20
Personal | 02:41:05
#### By Desktop &amp; Program
Desktop | Command | Time
------- | ------- | -----
Hacking | pidgin | 00:00:20
Personal | sublime_text | 01:10:50
Personal | terminator | 00:14:00
Personal | firefox | 01:16:10
Personal | idle | 00:09:35
Personal | fmp-pg.py --pause | 00:00:05
#### By Desktop &amp; Window
Desktop | Command | Window Title | Time
------- | ------- | ----- | -----
Hacking | pidgin | #python | 00:00:20
Personal | sublime_text | activity-logger • (activity-logger) - Sublime Text 2 | 00:04:10
Personal | sublime_text | untitled (activity-logger) - Sublime Text 2 | 00:00:20
Personal | sublime_text | ~/git/activity-logger/activity-logger.py (activity-logger) - Sublime Text 2 | 00:23:55
Personal | sublime_text | ~/git/activity-logger/activity-logger.py • (activity-logger) - Sublime Text 2 | 00:14:00
Personal | sublime_text | ~/git/activity-logger/reports/test.html (activity-logger) - Sublime Text 2 | 00:00:15
Personal | sublime_text | ~/git/activity-logger/templates/base.html (activity-logger) - Sublime Text 2 | 00:04:35
Personal | sublime_text | ~/git/activity-logger/templates/base.html • (activity-logger) - Sublime Text 2 | 00:03:45
Personal | sublime_text | ~/git/activity-logger/templates/daily.html (activity-logger) - Sublime Text 2 | 00:09:35
Personal | sublime_text | ~/git/activity-logger/templates/daily.html • (activity-logger) - Sublime Text 2 | 00:09:55
Personal | sublime_text | ~/git/activity-logger/templates/strapdown.js (activity-logger) - Sublime Text 2 | 00:00:20
Personal | terminator | erm@erm: ~/git | 00:00:20
Personal | terminator | erm@erm: ~/git/activity-logger | 00:11:35
Personal | terminator | erm@erm: ~/git/activity-logger/reports | 00:00:45
Personal | terminator | erm@erm: ~/git/activity-logger/reports/2014-11-28 | 00:00:05
Personal | terminator | erm@erm: ~/git/activity-logger/templates | 00:01:10
Personal | terminator | erm@erm: ~/git/volume-adjuster | 00:00:05
Personal | firefox | 7 Historical Figures Who Were Absurdly Hard To Kill &#124; Cracked.com - Mozilla Firefox | 00:00:10
Personal | firefox | Add null character to string in python - Stack Overflow - Mozilla Firefox | 00:00:35
Personal | firefox | Association Proxy — SQLAlchemy 0.9 Documentation - Mozilla Firefox | 00:00:25
Personal | firefox | Bootswatch: Cerulean - Mozilla Firefox | 00:00:20
Personal | firefox | Bootswatch: Default - Mozilla Firefox | 00:00:10
Personal | firefox | Bootswatch: Flatly - Mozilla Firefox | 00:00:20
Personal | firefox | Bootswatch: Free themes for Bootstrap - Mozilla Firefox | 00:00:20
Personal | firefox | Bootswatch: Journal - Mozilla Firefox | 00:00:10
Personal | firefox | Bootswatch: Paper - Mozilla Firefox | 00:00:20
Personal | firefox | Bootswatch: Sandstone - Mozilla Firefox | 00:00:10
Personal | firefox | Bootswatch: Simplex - Mozilla Firefox | 00:00:20
Personal | firefox | Character Entities - Symbols - Mozilla Firefox | 00:00:15
Personal | firefox | Create a New Repository - Mozilla Firefox | 00:02:50
Personal | firefox | Daily Activity - Mozilla Firefox | 00:21:55
Personal | firefox | Daily Activity 2014-11-28 - Mozilla Firefox | 00:09:30
Personal | firefox | Editing activity-logger/README.md at master · the7erm/activity-logger - Mozilla Firefox | 00:00:10
Personal | firefox | Filtering and Buffering — Mako 1.0.0 Documentation - Mozilla Firefox | 00:00:50
Personal | firefox | Finally someone noticed... - Mozilla Firefox | 00:00:30
Personal | firefox | Getting started · Bootstrap - Mozilla Firefox | 00:00:45
Personal | firefox | GitHub - Mozilla Firefox | 00:00:20
Personal | firefox | HTML Entities - Mozilla Firefox | 00:00:10
Personal | firefox | HTML UTF-8 Reference - Mozilla Firefox | 00:00:35
Personal | firefox | Homemade special dd - Mozilla Firefox | 00:00:30
Personal | firefox | Hostgator Black Friday / Cyber Monday Special Coupon &#124; www.promocodes.name - Mozilla Firefox | 00:00:10
Personal | firefox | Inheritance — Mako 1.0.0 Documentation - Mozilla Firefox | 00:01:10
Personal | firefox | Mako 1.0.0 Documentation - Mozilla Firefox | 00:00:20
Personal | firefox | Mozilla Firefox | 00:00:05
Personal | firefox | New File - Mozilla Firefox | 00:02:30
Personal | firefox | New Tab - Mozilla Firefox | 00:01:40
Personal | firefox | Object Relational Tutorial — SQLAlchemy 0.9 Documentation - Mozilla Firefox | 00:00:20
Personal | firefox | PHOTOS THAT ONLY CAT OWNERS WILL UNDERSTAND &#124; Gibba House - Mozilla Firefox | 00:01:10
Personal | firefox | Problem loading page - Mozilla Firefox | 00:00:10
Personal | firefox | Querying — SQLAlchemy 0.9 Documentation - Mozilla Firefox | 00:00:05
Personal | firefox | Raw Mako template included in another in Pylons - Stack Overflow - Mozilla Firefox | 00:00:20
Personal | firefox | Redirect to a Different URL using the Meta Tag "Refresh": Web Site Maintenance: Tools and Guides: IU Webmaster: Indiana University - Mozilla Firefox | 00:00:20
Personal | firefox | SQLAlchemy: how to filter date field? - Stack Overflow - Mozilla Firefox | 00:01:15
Personal | firefox | Search — Mako 1.0.0 Documentation - Mozilla Firefox | 00:00:15
Personal | firefox | Sesamii error:404 - theerm@gmail.com - Gmail - Mozilla Firefox | 00:00:20
Personal | firefox | Sqlalchemy -- Group by a relationship field - Stack Overflow - Mozilla Firefox | 00:00:40
Personal | firefox | Strapdown.js - Instant and elegant Markdown documents - Mozilla Firefox | 00:06:35
Personal | firefox | Syntax — Mako 1.0.0 Documentation - Mozilla Firefox | 00:02:50
Personal | firefox | The Mako Runtime Environment — Mako 1.0.0 Documentation - Mozilla Firefox | 00:00:20
Personal | firefox | Usage — Mako 1.0.0 Documentation - Mozilla Firefox | 00:03:00
Personal | firefox | Welcome &#124; Werkzeug (The Python WSGI Utility Library) - Mozilla Firefox | 00:00:05
Personal | firefox | Western Vista - Home - Mozilla Firefox | 00:00:10
Personal | firefox | activity-logger/README.md at master · the7erm/activity-logger - Mozilla Firefox | 00:00:20
Personal | firefox | arturadib/strapdown - Mozilla Firefox | 00:00:40
Personal | firefox | bootstrap cdn - Google Search - Mozilla Firefox | 00:00:10
Personal | firefox | bootstrap-markdown - cdnjs.com - the missing cdn for javascript and css - Mozilla Firefox | 00:00:30
Personal | firefox | cdnjs.com - the missing cdn for javascript and css - Mozilla Firefox | 00:00:05
Personal | firefox | html entities - Google Search - Mozilla Firefox | 00:00:05
Personal | firefox | html entities for pipe - Google Search - Mozilla Firefox | 00:00:05
Personal | firefox | html utf - Google Search - Mozilla Firefox | 00:00:05
Personal | firefox | javascript cdn markdown - Google Search - Mozilla Firefox | 00:00:35
Personal | firefox | mako - Google Search - Mozilla Firefox | 00:00:05
Personal | firefox | mako escape pound - Google Search - Mozilla Firefox | 00:00:05
Personal | firefox | mako for loop - Google Search - Mozilla Firefox | 00:00:05
Personal | firefox | mako inherit - Google Search - Mozilla Firefox | 00:00:05
Personal | firefox | mako python - Google Search - Mozilla Firefox | 00:00:05
Personal | firefox | mako raw block - Google Search - Mozilla Firefox | 00:01:05
Personal | firefox | mako raw html - Google Search - Mozilla Firefox | 00:00:20
Personal | firefox | mako trim - Google Search - Mozilla Firefox | 00:00:05
Personal | firefox | mako trim block - Google Search - Mozilla Firefox | 00:00:10
Personal | firefox | meta refresh - Google Search - Mozilla Firefox | 00:00:10
Personal | firefox | null python character - Google Search - Mozilla Firefox | 00:00:05
Personal | firefox | python - Encoding gives "'ascii' codec can't encode character … ordinal not in range(128)" - Stack Overflow - Mozilla Firefox | 00:00:10
Personal | firefox | python - Mark string as safe in Mako - Stack Overflow - Mozilla Firefox | 00:00:05
Personal | firefox | raw mako - Google Search - Mozilla Firefox | 00:00:05
Personal | firefox | sqlalchemy group by associative - Google Search - Mozilla Firefox | 00:00:05
Personal | firefox | sqlalchemy group by dict - Google Search - Mozilla Firefox | 00:00:05
Personal | firefox | strapdown js - Google Search - Mozilla Firefox | 00:00:30
Personal | firefox | strapdown/vendor/themes at gh-pages · arturadib/strapdown - Mozilla Firefox | 00:00:40
Personal | firefox | the7erm/activity-logger - Mozilla Firefox | 00:01:00
Personal | firefox | toopay/bootstrap-markdown - Mozilla Firefox | 00:00:50
Personal | firefox | welcome to Mako! - Mozilla Firefox | 00:01:20
Personal | firefox | werkzerbug - Google Search - Mozilla Firefox | 00:00:10
Personal | firefox | werkzeug - Google Search - Mozilla Firefox | 00:00:05
Personal | idle | idle | 00:09:35
Personal | fmp-pg.py --pause | Video-Player | 00:00:05

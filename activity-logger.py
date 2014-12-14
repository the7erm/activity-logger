#!/usr/bin/env python2
from subprocess import check_output, CalledProcessError
from time import sleep
from math import floor
from copy import deepcopy
import re
import pprint
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Date, DateTime,\
                       UniqueConstraint
from sqlalchemy.sql import select, func, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from datetime import date, datetime, timedelta
from sqlalchemy.orm import sessionmaker
from mako.template import Template
from mako.lookup import TemplateLookup

DAILY_TEMPLATE = Template(filename='templates/daily.html')

Base = declarative_base()
 
class ActivityLog(Base):
    __tablename__ = 'activity_log'
    __table_args__ = (
        UniqueConstraint('date', 'hour', 'workspace', 'command', 'title',
                         name='_date_hour_workspace_command_line_title_uc'),
    )
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    date = Column(Date())
    hour = Column(Integer())
    seconds = Column(Integer())
    workspace = Column(String(255))
    command = Column(String(255))
    title = Column(String(255))

    @property
    def hh_mm_ss(self):
        return hh_mm_ss(self.seconds)


    def __repr__(self):
        return ("<ActivityLog(date='%r',\n"
                "             hour=%d,\n"
                "             seconds=%d,\n"
                "             workspace='%r',\n"
                "             command='%r'\n"
                "             title='%r'\n"
                "             time:%s"
                ")>" % (self.date, self.hour, self.seconds, self.workspace,
                        self.command, self.title, hh_mm_ss(self.seconds)))


# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine('sqlite:///activity.db')
engine.raw_connection().connection.text_factory = unicode
 
# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

RE_WMCTRL_DESKTOP = re.compile('([0-9]+)\s+([\*\-])\s+(DG\:\ .*)\s+(VP\: .*)\s+(WA\: .*)\s+([0-9x]+)\s+(.*)')
RE_WMCTRL_OPEN_PROGRAMS = re.compile("([0-9xa-f]+)\s+([\-0-9]+)\s+([0-9]+)\s+([A-Za-z0-9\_\-]+)\s+(.*)")

RE_XLSCLIENTS = re.compile("Window\ ([0-9a-fx]+)\:\n" 
                           "\ \ Machine\:\ \ (.*)\n"
                           "\ \ Name\:\ \ (.*)\n"
                           "\ \ Command\:\ \ (.*)\n"
                           "\ \ Instance\/Class\:  (.*)")

def print_r(obj):
    pprint.pprint(obj)

def get_idle():
    idle_ms = int(safe_check_output(*['xprintidle']))
    idle_sec = floor(idle_ms / 1000)
    return int(idle_sec)

def get_active_desktop():
    output = safe_check_output(*['wmctrl', '-d'])
    lines = output.split("\n")
    # 0  * DG: 1280x720  VP: 0,0  WA: 0,43 2960x857  Personal

    for l in lines:
        match = RE_WMCTRL_DESKTOP.match(l)
        if match:
            # print match.groups()
            if match.group(2) == '*':
                return int(match.group(1)), match.group(7)

def get_xlsclients():
    output = safe_check_output(*['xlsclients', '-la'])
    """
    Window 0x4600206:
      Machine:  erm
      Name:  skype
      Command:  skype
      Instance/Class:  skype/Skype"""

    clients = {}
    for match in RE_XLSCLIENTS.finditer(output):
        # print "Match:", match
        if match:
            # print "groups:", match.groups()
            window_id = match.group(1)
            clients[window_id] = {
                "Window": window_id,
                "Machine": match.group(2),
                "Name": match.group(3),
                "Command": match.group(4),
                "Instance_Class": match.group(5)
            }

    return clients

def safe_check_output(*args, **kwargs):
    try:
        output = check_output(args)
    except CalledProcessError, err:
        print "CalledProcessError: %s %s" % (err, args)
        return ""

    return output

def get_open_windows(desktop_number=None, only_active=False):
    
    """
    wmctrl -lp
    0x0387af21  3 2893   erm Source of: file:///home/erm/git/activity-logger/reports/2014-11-28/daily.html - Mozilla Firefox
    """

    try:
        active_pid = check_output(["xdotool", 
                                   "getwindowfocus", 
                                   "getwindowpid"]).strip()
    except CalledProcessError:
        active_pid = None
        if only_active:
            return []

    output = safe_check_output(*['wmctrl', '-lp'])
    lines = output.split("\n")
    # 0  * DG: 1280x720  VP: 0,0  WA: 0,43 2960x857  Personal
    # clients = get_xlsclients()
    # print_r(clients)
    open_windows = []
    processed_pids = []
    for l in lines:
        match = RE_WMCTRL_OPEN_PROGRAMS.match(l)
        # print "match:",match
        if match:
            window_id = match.group(1)
            group_desktop_number = int(match.group(2))
            pid = match.group(3)
            user = match.group(4)
            title = match.group(5)
            
            active = bool(active_pid == pid)
            # Only process active window
            if only_active and not active:
                continue

            # Only process pids that are on the current desktop
            if desktop_number is not None and \
               group_desktop_number != desktop_number:
                continue

            if pid in processed_pids:
                # Only process a pid once. Some process have more than 1
                # window.
                continue
            processed_pids.append(pid)

            # Convert the title so it'll play nicely with sqlite.
            if not isinstance(title, unicode):
                title = title.decode("utf-8")

            title_lower = title.lower()
            for find, replace in REPLACE_RULES:
                if isinstance(find, str):
                    if find.lower() in title_lower:
                        # print "REPLACE:", title, "=>", replace
                        title = replace
                        break
                elif find.match(title):
                    # print "REPLACE:", title, "=>", replace
                    title = replace
                    break

            proc_path = os.path.join("/proc", pid)
            exe_path = os.path.join(proc_path, 'exe')
            cmd_path = os.path.join(proc_path, 'cmdline')
            realpath = os.path.realpath(exe_path)
            command_line = "error"
            with open(cmd_path,'r') as fp:
                command_line = fp.read()
                command_line = command_line.rstrip("\x00")
            
            command = os.path.basename(realpath)
            
            window_data = {
                "window_id": window_id,
                "desktop_number": group_desktop_number,
                "pid": pid,
                "user": user,
                "window_title": title,
                "command": command,
                "active": active,
                "command_line": command_line
            }
            
            open_windows.append(window_data)
            if only_active:
                # Save processing we only need to get the first one
                # If only_active is set.
                break

    return open_windows



def report(today=None):
    if today is None:
        today = date.today()
    ESC = chr(27)
    # print "{ESC}[2J{ESC}[0;0H".format(ESC=ESC)
    print "*"*20

    activity = session.query(ActivityLog.workspace, 
                             ActivityLog.command,
                             func.sum(ActivityLog.seconds))\
                      .filter(ActivityLog.date == today)\
                      .group_by(ActivityLog.workspace, 
                                ActivityLog.command)

    workspace = ""
    total_seconds = 0
    for a in activity:
        # print_r(a)
        if a[0] != workspace:
            if total_seconds:
                print "%s %s" % (workspace, hh_mm_ss(total_seconds))
            workspace = a[0]
            total_seconds = 0
            print "-=[ %s ]=-" % workspace
        print hh_mm_ss(a[2]), a[1]
        total_seconds += a[2]

    print "%s %s" % (workspace, hh_mm_ss(total_seconds))

    spec = and_(ActivityLog.date == today, 
                ActivityLog.command != "idle")
    daily = session.query(ActivityLog.workspace, ActivityLog.date,
                             func.sum(ActivityLog.seconds))\
                      .filter(spec)\
                      .group_by(ActivityLog.date, 
                                ActivityLog.workspace)

    print "By Workspace"
    _date = ""
    for a in daily:
        if _date != a[1]:
            _date = a[1]
            print "-[ %s ]-" % _date
        print hh_mm_ss(a[2]), a[0]

def workspace_active_data(today=None):
    if today is None:
        today = date.today()

    spec = and_(ActivityLog.date == today, 
                ActivityLog.command != "idle")
    cols = ['Workspace', 'Time']
    title = "Workspace - Active"
    res = session.query(ActivityLog.workspace,
                        func.sum(ActivityLog.seconds))\
                 .filter(spec)\
                 .group_by(ActivityLog.date, 
                           ActivityLog.workspace)
    return {
        "title": title,
        "cols": cols,
        "data": res
    }

def workspace_command_title_data(today=None):
    if today is None:
        today = date.today()

    spec = and_(ActivityLog.date == today)
    cols = ['Workspace', 'Command', 'Title', 'Time']
    title = "Workspace, Command and Title"
    res = session.query(ActivityLog.workspace, 
                        ActivityLog.command, 
                        ActivityLog.title,
                        func.sum(ActivityLog.seconds))\
                 .filter(spec)\
                 .group_by(ActivityLog.workspace,
                           ActivityLog.command,
                           ActivityLog.title)
    return {
        "title": title,
        "cols": cols,
        "data": res
    }

def workspace_command_data(today=None):
    if today is None:
        today = date.today()

    spec = and_(ActivityLog.date == today)
    cols =   ['Workspace', 'Command', 'Time']
    
    title = "Workspace & Command"
    res = session.query(ActivityLog.workspace, 
                        ActivityLog.command,
                        func.sum(ActivityLog.seconds))\
                 .filter(spec)\
                 .group_by(ActivityLog.workspace,
                           ActivityLog.command)

    return {
        "title": title,
        "cols": cols,
        "data": res
    }

def workspace_hour_data_active(today=None):
    if today is None:
        today = date.today()

    spec = and_(ActivityLog.date == today,
                ActivityLog.command != "idle")
    cols =   ['Workspace', 'Hour', 'Time']
    title = "Workspace & Hour - Active"
    res = session.query(ActivityLog.workspace, 
                        ActivityLog.hour,
                        func.sum(ActivityLog.seconds))\
                 .filter(spec)\
                 .group_by(ActivityLog.workspace,
                           ActivityLog.hour)

    return {
        "title": title,
        "cols": cols,
        "data": res
    }

def make_dashes(cols):
    dashes = []
    for col in cols:
        dashes.append("-"*len(col))
    return dashes

def command_data(today=None):
    if today is None:
        today = date.today()

    spec = and_(ActivityLog.date == today)
    cols = ['Command', 'Time']
    title = "Command"
    res = session.query(ActivityLog.command,
                        func.sum(ActivityLog.seconds))\
                 .filter(spec)\
                 .group_by(ActivityLog.command)
    return {
        "title": title,
        "cols": cols,
        "data": res
    }


def print_row(row, cols):
    # print "ROW:",row
    # print "COLS",cols
    data = []
    for i, col in enumerate(row):
        try:
            col_title = cols[i]
        except IndexError,err:
            col_title = "IndexError:%s index:%i" % (err, i)

        if col_title == 'Time':
            data.append(hh_mm_ss(col))
            continue
        if col_title == 'Hour':
            data.append("%02d:00" % col)
            continue

        if col_title == 'Command':
            parts = col.split("\x00")
            basename = os.path.basename(parts[0])
            space_parts = basename.split(" ")
            basename = space_parts[0]
            if basename in ('python', 'python2', 'python3'):
                #   u'/usr/bin/python\x00/usr/bin/terminator' basename:u'python'
                basename = os.path.basename(parts[1])
                # scontinue
            data.append("%s" % (basename,))

            continue

        _str =  "%s" % col
        _str = _str.replace("|", "&#124;")
        data.append(_str)
    return " | ".join(data)


def get_week_bounds(today=None):
    if today is None:
        today = date.today()
    # For example, 2004 begins on a Thursday, so the first week of ISO year 2004 begins on Monday, 29 Dec 2003 and ends on Sunday, 4 Jan 2004, so that date(2003, 12, 29).isocalendar() == (2004, 1, 1) and date(2004, 1, 4).isocalendar() == (2004, 1, 7).

    one_day = timedelta(days=1)
    first_day = deepcopy(today)
    last_day = deepcopy(today)
    print "today:", today
    if first_day.strftime("%w") == "0":
        # The first day is Sunday
        return first_day, (last_day + timedelta(days=6))

    while weeks_match((first_day - one_day), today):
        # count down days until the week changes
        first_day = first_day - one_day

    print (first_day - one_day).strftime("%W") == today.strftime("%W"),\
          (first_day - one_day).strftime("%W"),' == ', today.strftime("%W")

    while weeks_match((last_day + one_day), today):
        # count up days until the week changes
        last_day = last_day + one_day

    print (last_day + one_day).strftime("%W") == today.strftime("%W"), \
          (last_day + one_day).strftime("%W"),' == ', today.strftime("%W")

    if first_day.strftime("%w") != "0":
        first_day = first_day - one_day

    last_day = last_day - one_day
    print "first_day:", first_day.strftime("%c")
    print "last_day:", last_day.strftime("%c")

    return first_day, last_day

def date_key(date, today=None):
    if today is None:
        today = date.today()

    if date is None:
        return ""

    if date != today:
        return date.strftime(
            "<a href='../%Y-%m-%d/daily.html'>%Y-%m-%d %a</a>")
    
    return date.strftime("<a href='../%Y-%m-%d/daily.html'><b>%Y-%m-%d %a</b></a>")

def weekly_breakdown(today=None):
    if today is None:
        today = date.today()

    low, high = get_week_bounds(today=today)
    print "low:", low
    print "high:", high

    spec = and_(ActivityLog.command != "idle",
                ActivityLog.date >= low,
                ActivityLog.date <= high)
    cols = ['Workspace']
    dates = []

    title = "Weekly - Active"
    res = session.query(ActivityLog.workspace, 
                        ActivityLog.date,
                        func.sum(ActivityLog.seconds))\
                 .filter(spec)\
                 .group_by(ActivityLog.workspace,
                           ActivityLog.date)\
                 .order_by(ActivityLog.date.asc(), ActivityLog.workspace.asc())

    date_data = {}
    numdays = 7
    date_list = [low + timedelta(days=x) for x in range(0, numdays)]
    date_list = sorted(date_list)
    print "date_list:", date_list

    for d in date_list:
        _date = date_key(d, today)
        if _date not in dates:
            dates.append(_date)

        if _date not in cols:
            cols.append(_date)

    for r in res:
        _date = date_key(r.date, today)
        if r.workspace not in date_data:
            date_data[r.workspace] = {}

        print_r(r)
        date_data[r.workspace][_date] = "%s" % (hh_mm_ss(r[2]),)
        if r.date == today:
            date_data[r.workspace][_date] = "<b>%s</b>" % (hh_mm_ss(r[2]), )


    for workspace in date_data:
        for _date in dates:
            if _date not in date_data[workspace]:
                date_data[workspace][_date] = " "

        for d in date_list:
            _date = date_key(d, today)
            if _date not in date_data[workspace]:
                date_data[workspace][_date] = " "

    """
    {u'Hacking': {'2014-11-28 Fri': '00:00:40', '2014-11-29 Sat': ' '},
     u'Personal': {'2014-11-28 Fri': '05:01:05', '2014-11-29 Sat': '00:40:20'},
     u'Programing': {'2014-11-28 Fri': '02:51:50', '2014-11-29 Sat': ' '},
     u'Sesamii': {'2014-11-28 Fri': '00:34:15', '2014-11-29 Sat': ' '},
     u'Task': {'2014-11-28 Fri': '01:58:05', '2014-11-29 Sat': '00:54:20'}}
    """

    print_r(date_data)
    date_data_formatted = []
    for workspace in date_data:
        row = [workspace]
        keys = date_data[workspace].keys()
        keys = sorted(keys)
        print "keys:", 
        print_r(keys)
        for _date in keys:
            row.append(date_data[workspace][_date])
        date_data_formatted.append(row)
        print " | ".join(row)

    print_r(date_data_formatted)
    """
    GOAL
                | Sun   | Mon | Tue | Wed | Thru | Fri | Sat
    ------------| ----- | --- | --- | --- | ---- | --- | ---
    workspace 1 | 00:00 |
    workspace 2 |
    workspace 3 |
    """
    print "COLS"
    print_r(cols)

    return {
        "title": title,
        "cols": cols,
        "data": date_data_formatted
    }

def get_yesterday(today=None):
    if today is None:
        today = date.today()

    spec = and_(ActivityLog.date < today)
    res = session.query(ActivityLog.date)\
                 .filter(spec)\
                 .group_by(ActivityLog.date)\
                 .order_by(ActivityLog.date.desc())\
                 .first()

    if res:
        print "yesterday:", res[0]
        return res[0]
    return None

def get_tomorrow(today=None):
    if today is None:
        today = date.today()

    spec = and_(ActivityLog.date > today)
    res = session.query(ActivityLog.date)\
                 .filter(spec)\
                 .group_by(ActivityLog.date)\
                 .order_by(ActivityLog.date.asc())\
                 .first()

    if res:
        print "tomorrow:", res[0]
        return res[0]
    # _today = get.today()
    # one_day = timedelta(days=1)
    # tomorrow = today + one_day
    return None

def get_next_week(today=None):
    if today is None:
        today = date.today()

    next_week = today + timedelta(days=7)
    first, last = get_week_bounds(next_week)
    first = first - timedelta(days=1)
    day_with_activity = get_tomorrow(first)
    return day_with_activity

def get_last_week(today=None):
    if today is None:
        today = date.today()

    last_week = today - timedelta(days=7)
    first, last = get_week_bounds(last_week)
    first = first - timedelta(days=1)
    day_with_activity = get_tomorrow(first)
    if day_with_activity == today:
        return None
    return day_with_activity


def weeks_match(date1, date2):
    if not isinstance(date1, date) or not isinstance(date2, date):
        return False

    if date1 == date2:
        return True

    return date1.strftime("%W") == date2.strftime("%W")


def get_all_days_with_activity():
    low_date = session.query(ActivityLog.date)\
                      .order_by(ActivityLog.date.asc())\
                      .first()

    high_date = session.query(ActivityLog.date)\
                      .order_by(ActivityLog.date.desc())\
                      .first()

    if not low_date or not high_date:
        return []

    low, end_date = get_week_bounds(high_date[0])

    days = []
    _date = low_date.date
    while _date <= end_date:
        days.append(_date)
        _date += timedelta(days=1)
    return days


def write_report(today=None):
    if today is None:
        today = date.today()

    by = []
    by.append(weekly_breakdown(today=today))
    by.append(workspace_active_data(today=today))
    by.append(workspace_hour_data_active(today=today))
    by.append(workspace_command_data(today=today))
    by.append(command_data(today=today))
    by.append(workspace_command_title_data(today=today))
    # print_r(weekly_breakdown())

    mylookup = TemplateLookup(directories=['templates'], 
                              output_encoding='utf-8', 
                              encoding_errors='replace')

    DAILY_TEMPLATE = mylookup.get_template("daily.html")

    
    

    yesterday = get_yesterday(today=today)
    tomorrow = get_tomorrow(today=today)
    
    title = "Daily Activity %s" % today

    next_week = get_next_week(today)
    last_week = get_last_week(today)

    html = DAILY_TEMPLATE.render(title=title,
                                 hh_mm_ss=hh_mm_ss, 
                                 by=by,
                                 basename=os.path.basename,
                                 make_dashes=make_dashes,
                                 print_row=print_row,
                                 yesterday=yesterday,
                                 today=today,
                                 tomorrow=tomorrow,
                                 last_week=last_week,
                                 next_week=next_week)

    report_dir = os.path.join("reports/","%s" % today)
    report_file = os.path.join(report_dir, "daily.html")
    if not os.path.exists(report_dir):
        os.makedirs(report_dir, 0o777)

    with open(report_file, 'w') as fp:
        fp.write(html)


def hh_mm_ss(s):
    h = floor(s / 3600.0)
    s = s - (h * 3600)
    m = floor(s / 60.0)
    s = s - (m * 60)
    return "%02d:%02d:%02d" % (h,m,s)

def log_append_activity(current_activity):
    # print "send to sql"
    # print "current_activity:"
    # print_r(current_activity)
    try:
        command_line = current_activity['active_window'][0]["command_line"]
        title = current_activity['active_window'][0]["window_title"]
    except:
        command_line = "None"
        title = "None"

    try:
        workspace = current_activity['workspace']
    except:
        workspace = "None"

    spec = {
        "date": date.today(),
        "hour": datetime.now().hour,
        "workspace": workspace,
        "command": command_line,
        "title": title
    }

    activity_log = session.query(ActivityLog).filter_by(**spec).first()

    if not activity_log:
        spec["seconds"] = TIME_BETWEEN_CHECKS
        activity_log = ActivityLog(**spec)
    else:
        activity_log.seconds += TIME_BETWEEN_CHECKS

    # print activity_log

    session.add(activity_log)
    session.commit()

IDLE_THRESHOLD = 90
DEBUG = False
TIME_BETWEEN_CHECKS = 10

# string/regex, replacement
REPLACE_RULES = [
    (re.compile("Inbox \(\d+\) .* Gmail"), "Inbox - Gmail"),
    ("(Private Browsing)", "--hidden--"),
    ("banking", "--hidden--"),
    ("western vista", "--hidden--")
]

days = get_all_days_with_activity()
for d in days:
    print d
    write_report(d)

now = datetime.now()
write_report()
while True:
    # write_report()
    idle_sec = get_idle()
    active_desktop_number, active_desktop = get_active_desktop()
    active_windows = get_open_windows(active_desktop_number, True)
    # print "active_desktop_number:", active_desktop_number
    if idle_sec >= IDLE_THRESHOLD:
        # print "idle_sec:", idle_sec
        log_append_activity({
            "workspace": active_desktop,
            "active_window": [{
                "command": "idle",
                "window_title": "idle",
                "command_line": "idle",
                "title": "idle"
            }]
        })
    else:
        log_append_activity({
            "workspace": active_desktop,
            "active_window": active_windows
        })
    report()

    if now.minute != datetime.now().minute:
        write_report()
        now = datetime.now()

    sleep(TIME_BETWEEN_CHECKS)

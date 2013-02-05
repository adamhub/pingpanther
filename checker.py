#! /usr/bin/python -u
#@+leo-ver=5-thin
#@+node:climber.20111230205203.1319: * @thin monicheck.py
#@@first

#version 0.11b

#Originally authored by pulsh.com
#
#This file is part of Pingpanther.
#
#Pingpanther is free software: you can redistribute it and/or modify
#it under the terms of the GNU Affero General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#Pingpanther is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU Affero General Public License for more details.
#
#You should have received a copy of the GNU Affero General Public License
#along with Pingpanther.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys
import logging
from httplib import HTTPConnection, socket
import smtplib
import sqlite3
import urlparse
from email.mime.text import MIMEText
from datetime import datetime, timedelta
from settings import DB_FILE, TWILIO_ACCOUNT, TWILIO_TOKEN
import urllib2
import urllib

conn = None
cur = None


def init_db():

    global conn
    global cur

    def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    try:
        conn = sqlite3.connect(DB_FILE, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        conn.row_factory = dict_factory
        cur = conn.cursor()
    except:
        print 'db error'
        exit(1)


def get_previous_cron_status():
    '''RUNNING or STOPPED'''

    r = cur.execute('select max(created_on) as "last_run [timestamp]", CURRENT_TIMESTAMP as "cts [timestamp]" from last_run').fetchone()

    if r['last_run'] is None:
        return 'STOPPED'

    settings = get_settings()
    minutes = int(settings['cron']['frequency'])
    frequency = timedelta(minutes)
    since_last_run = r['cts'] - r['last_run']

    # If time interval since last run is greater than frequency of cron jobs
    if since_last_run > frequency:
        return 'STOPPED'
    else:
        return 'RUNNING'


def get_settings():
    cur = conn.cursor()
    sql = "SELECT * FROM settings"
    settings_list = cur.execute(sql).fetchall()

    d = {}

    for setting in settings_list:
        section = setting['section']
        field = setting['field']
        value = setting['value']

        if section in d:
            d[section][field] = value
        else:
            d[section] = {field: value}

    return d


def get_sites():
    cur.execute('select * from site')
    sites = cur.fetchall()
    cur.close()
    return sites


def get_response(url):
    '''Return response object from URL'''
    try:
        conn = HTTPConnection(url, 80)
        conn.request("HEAD", "/")
        return conn.getresponse()
    except socket.error:
        return None
    except:
        return None


def is_internet_reachable(url_field):
    settings = get_settings()
    site = settings['internet_on'][url_field]

    response = get_response(site)
    if response is None:
        return False

    if response.status == 200 or str(response.status).startswith('3'):
        return True

    return False


def update_settings(section, field, value):
    cur.execute("UPDATE settings SET value = ? WHERE section = ? AND field = ?",
        (value, section, field))
    conn.commit()
    cur.close()


def check_site_state(url):
    if url.startswith('http://'):
        url = urlparse.urlparse(url).netloc

    response = get_response(url)
    if response is None:
        return 'down'
    if response.status == 200 or response.status == 302 or response.status == 403 or response.status == 301 or response.status == 401:
        return 'up'

    return 'down'


def update_site(site, new_state):
    if site['current_state'] != new_state:
        cur = conn.cursor()
        sql = "UPDATE site SET current_state = ?, state_changed_on = CURRENT_TIMESTAMP where id = ?"
        cur.execute(sql, (new_state, site['id']))
        conn.commit()
        cur.close()
        cur = conn.cursor()
        sql = "INSERT INTO [check] (site_id, state, created_on) VALUES (?, ?, CURRENT_TIMESTAMP)"
        cur.execute(sql, (site['id'], new_state))
        conn.commit()
        send_email(site, new_state)
        send_zapier_trigger(site['url'], new_state)
        cur.close()
        if new_state == 'down':
            cur = conn.cursor()
            sql = "INSERT INTO down_times (site_id, time_down) VALUES (?, ?)"
            cur.execute(sql, (site['id'], site['created_on']))
            conn.commit()
            cur.close()


def send_email(site, new_state):

    try:
        settings = get_settings()
        #Get Email Notification fields
        email_keys = filter(lambda k: 'email' in k, settings['notifications'].keys())
        email_keys.sort()
        email_list = []
        for email_key in email_keys:
            email_list.append(settings['notifications'][email_key])
        toaddrs = ';'.join(email_list)
        if not toaddrs:
            return

        server = settings['mailserver']['server']
        port = settings['mailserver']['port']
        username = settings['mailserver']['username']
        password = settings['mailserver']['password']
        sender = settings['mailserver']['email_from']
        if not sender:
            sender = 'pingpanther@localhost'

        if not port:
            port = 25
        if not server:
            return

        msg = 'Status of %s site has changed from %s to %s' % (site['url'], site['current_state'], new_state)
        msg = MIMEText(msg)
        msg['Subject'] = 'Pingpanther: %s is %s!' % (site['url'], new_state)
        msg['From'] = sender
        msg['To'] = toaddrs

        server = smtplib.SMTP(server, int(port))
        if username and password:
            server.login(str(username), str(password))

        server.sendmail(sender, [toaddrs], msg.as_string())
        server.quit()
        print 'Mail send successfully!'
    except Exception, err:
        print 'Mail failed', str(err)


def send_test_email():
    try:
        settings = get_settings()
        #Get Email Notification fields
        email_keys = filter(lambda k: 'email' in k, settings['notifications'].keys())
        email_keys.sort()
        email_list = []
        for email_key in email_keys:
            email_list.append(settings['notifications'][email_key])
        toaddrs = ';'.join(email_list)
        if not toaddrs:
            return
        
        server = settings['mailserver']['server']
        port = settings['mailserver']['port']
        username = settings['mailserver']['username']
        password = settings['mailserver']['password']
        sender = settings['mailserver']['email_from']
        if not sender:
            sender = 'pingpanther@localhost'

        if not port:
            port = 25
        if not server:
            return
        
        msg = """Good News! Your email settings are correct if you are reading this.
        
        - The Panther has spoken
        
        http://pingpanther.org
        """
        msg = MIMEText(msg)
        msg['Subject'] = 'Test email from PingPanther'
        msg['From'] = sender
        msg['To'] = toaddrs

        server = smtplib.SMTP(server, int(port))
        if username and password:
            server.login(str(username), str(password))

        server.sendmail(sender, [toaddrs], msg.as_string())
        server.quit()
        print 'Mail send successfully!'
        
    except Exception, err:
        print 'Mail Failed', str(err)


def save_last_run():
    sql = "INSERT INTO last_run (created_on) VALUES (CURRENT_TIMESTAMP)"
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    cur.close()

    sql = 'SELECT Count(*) as row_count FROM [last_run]'
    cur = conn.cursor()
    if cur.execute(sql).fetchone()['row_count'] > 20:
        sql = 'delete from last_run where id not in (select id from last_run order by id desc limit 20)'
        cur.execute(sql)
        conn.commit()
        cur.close()


def send_zapier_trigger(site_url, new_state):
    """ Sends/Triggers a zapier service to trigger the gtalk request. """
    site_data = "%s is %s" % (site_url, new_state)
    req = urllib2.Request('https://zapier.com/hooks/catch/n/i5xa/', 'message=%s' % site_data)
    rs = urllib2.urlopen(req)
    print str(rs.read())


def main():

    try:
        init_db()

        if is_internet_reachable('url1') or is_internet_reachable('url2'):
            sites = get_sites()
            for site in sites:
                state = check_site_state(site['url'])
                update_site(site, state)
                print site['url'], state
        else:
            print 'Either the world ended or we are not connected to the net.'

        save_last_run()

        ''' closes db connection '''
        conn.close()

    except Exception, err:
        print str(err)
        raise


if __name__ == '__main__':
    main()

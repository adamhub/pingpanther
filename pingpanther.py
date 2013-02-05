#! /usr/bin/python -u
#@+leo-ver=5-thin
#@+node:climber.20111226160435.1316: * @thin pingpanther.py
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

import urlparse
import time
import sqlite3
import os
import sys
import math
import csv
import tarfile
import urllib
import urllib2

from uuid import uuid4
from distutils import dir_util
from urllib2 import urlopen
from datetime import datetime
from datetime import timedelta
from httplib import HTTPConnection, socket
from bottle import run, template, static_file, request,\
    debug, redirect, route, install, response, abort
from tools.bottle_sqlite import SQLitePlugin
from tools.utils import unique_list, set_password, check_password
from migrator import run_migrations
from settings import DB_FILE, PINGPANTHER_ROOT, CRON_FREQUENCY,\
    UPDATE_URL, COOKIES_SECRET_KEY

runAsCGI = 'SCRIPT_NAME' in os.environ
url_base = os.environ.get('SCRIPT_NAME', '')

install(SQLitePlugin(dbfile=DB_FILE))

debug(True)


def check_db():
    return os.path.exists(DB_FILE)


@route('/test-email/<option:re:[a-z]+>', method='POST')
def send_test_email(db, option):
    if option == 'python':
        from checker import send_email, init_db
        init_db()
        send_email([], '', True)
        redirect('/settings')
    elif option == 'php':
        url = "http://templeclan.com/pingpanther/send_mail.php?do=send"
        data = urllib.urlencode({
            'to_email': 'ionic.acid25@gmail.com',
        })
        req = urllib2.Request(url, data)
        urllib2.urlopen(req)
        redirect('/pingpanther/pingpanther.py/settings')

@route('/<tablename:re:[a-z]+>/csv', method='GET')
def export_csv(db, tablename):
    #there will be somewhat a switch here
    if tablename == 'site' or tablename == 'settings':
        filename = '%s.csv' % tablename

        filepath = os.path.join(PINGPANTHER_ROOT + '/', filename)
        outfile = open(filepath, 'wb')
        exports = db.execute("SELECT * FROM %s" % tablename).fetchall()
        csv_writer = csv.writer(outfile, delimiter=',')

        csv_writer.writerow(exports[0].keys())

        for export in exports:
            csv_writer.writerow([item for item in export.__iter__()])

        outfile.close()

        return static_file(filename, root=PINGPANTHER_ROOT + '/',\
            download=filename)
    abort(404, 'No such tablename.')


@route('/import/<tablename:re:[a-z]+>/csv', method='POST')
def import_csv(db, tablename):
    #there will be somewhat a switch here as well.
    if tablename == 'site' or tablename == 'settings':
        try:
            the_file = request.files.get('file-0')
            reader = csv.reader(the_file.file)
            rownum = 0
            for row in reader:
                # Save header row.
                if rownum == 0:
                    header = row
                else:
                    colnum = 0
                    for col in row:
                        #for the sites
                        if header[colnum] == 'url':
                            exec_db = "SELECT * FROM %s where url=%s"\
                                % (tablename, "'" + col + "'")
                            exports = db.execute(exec_db).fetchall()
                            exec_db = "INSERT INTO %s (%s) VALUES (%s)"\
                                % (tablename, ','.join(header),
                                ','.join(["'" + item + "'" for item in row]))
                            if len(exports) == 0:
                                new_id = db.execute(exec_db).lastrowid
                                print new_id
                        #for the settings
                        if header[colnum] == 'section'\
                            or header[colnum] == 'field':

                            exec_db = 'SELECT value from %s'\
                                'where section="%s" and field="%s"' %\
                                (tablename, row[0], row[1])
                            the_value = db.execute(exec_db).fetchone()
                            if the_value:
                                if [value for value in the_value.__iter__()][0] == '':
                                    new_id = db.execute('UPDATE %s SET value="%s" where section="%s" and field="%s"' %\
                                        (tablename, row[2], row[0], row[1])).lastrowid
                                    print new_id
                            else:
                                new_id = db.execute("INSERT INTO %s (%s) VALUES (%s)" %\
                                    (tablename, ','.join(header),
                                    ','.join(["'" + item + "'" for item in row]))).lastrowid

                        colnum += 1
                rownum += 1
            return {
                'message': 'success'
            }
        except Exception, err:
            print err
            pass
    return {
        'message': 'fail'
    }


def convert_to_localdate(dt, db):
    settings = get_settings(db)
    hours = int(settings['timezone']['difference'])
    local_date = dt + timedelta(hours)

    return local_date


def tmpl(template_name, **kw):
    #we need to pass url_base to all templates

    kw['url_base'] = url_base
    return template(template_name, **kw)


def pretty_date(time):
    now = datetime.utcnow()
    if type(time) is int:
        time = datetime.fromtimestamp(time)
    diff = (now - time)
    seconds = diff.seconds
    days = diff.days

    if days == 0:
        if seconds < 60:
            return str(seconds) + ' secs'
        elif seconds < 3600:
            return str(seconds / 60) + ' mins'
        elif seconds < 7200:
            return '1 hr'
        else:
            return str(seconds / 3600) + ' hrs'
    else:
        if days == 1:
            return '1 day'
        else:
            return str(days) + ' days'


def get_response(url):
    '''Return response object from URL'''
    try:
        conn = HTTPConnection(url, 80)
        conn.request('HEAD', '/')
        return conn.getresponse()
    except socket.error:
        return None
    except:
        return None


def check_site_state(url):
    if url.startswith('http://'):
        url = urlparse.urlparse(url).netloc

    response = get_response(url)
    if response is None:
        return 'down'

    if response.status == 200 or response.status == 302 or response.status == 403:
        return 'up'

    return 'down'


def set_settings(db, settings):
    for section, field_value in settings.items():
        for field, value in field_value.items():
            db.execute("UPDATE settings SET value = ? WHERE section=? and field = ?", (value, section, field))


def get_settings(db):
    sql = "SELECT * FROM settings"
    settings_list = db.execute(sql).fetchall()

    d = {}

    for section, field, value in settings_list:
        if section in d:
            d[section][field] = value
        else:
            d[section] = {field: value}

    return d


def tags_string(tag_list):
    """Returns a string of links for every tag"""
    tags_string = ""
    for tag in tag_list:
        if tag != "":
            tags_string = tags_string + (
                "<a href='%s?tag_filter=%s'>%s</a>, " % (url_base, tag,
                    tag))
    if tags_string != "":
        tags_string = tags_string[:len(tags_string) - 1]
    return str(tags_string)


def tag_weight(db, tag, biggest_tag_count):
    tagged_count = db.execute("SELECT COUNT(*) AS count FROM \
                    tagged_item WHERE tag = ?",
                    (tag['key'],)).fetchone()['count']
    min_font = 13
    max_font = 24
    if tagged_count <= 0:
        # avoid math errors
        tagged_count = 1
    ctag = float(math.log10(tagged_count))
    btag = float(math.log10(biggest_tag_count))
    if btag <= 0:
        # avoid math errors
        btag = 1
    tag_font = int(ctag / btag * (max_font - min_font) + min_font)
    return tag_font


def generate_tag_cloud(db):
    all_tags = db.execute("SELECT * FROM tags").fetchall()
    biggest_tag = db.execute(
        "SELECT item, COUNT(item) AS count FROM tagged_item \
        GROUP BY item ORDER BY count DESC").fetchone()
    if biggest_tag:
        biggest_tag_count = biggest_tag['count']
    else:
        biggest_tag_count = 1
    tag_cloud = []
    for tag in all_tags:
        tag = dict(tag)
        tag['font_size'] = tag_weight(db, tag, biggest_tag_count)
        tag_cloud.append(tag)
    return tag_cloud


@route('/tag_cloud', method='GET')
def tag_cloud(db):
    """Returns a tag cloud json"""
    # tag cloud setup
    tag_cloud = generate_tag_cloud(db)
    return {
        'tag_cloud': tag_cloud,
    }


@route('/media/<filename>')
def server_static(filename):
    """Static file access
    """
    return static_file(filename, root='./media')


def get_email_keys(settings):
    #Get Email Notification fields
    email_keys = filter(lambda k: 'email' in k, settings['notifications'].keys())
    email_keys = sorted(email_keys, key=lambda email: int(email.split('email')[1]), reverse=False)
    return email_keys


@route('/site/add', method='POST')
def add(db):
    """Adds a new site to track"""
    try:
        url = request.POST.get('url')
        frequency = request.POST.get('frequency')
        fail_trigger = request.POST.get('fail_trigger')
        respond_seconds = request.POST.get('respond_seconds')
        state = check_site_state(url)
        new_id = db.execute(
            "INSERT INTO site (url, frequency, respond_seconds, \
            fail_trigger, current_state, state_changed_on, created_on) \
            VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP, \
            CURRENT_TIMESTAMP)", (url, frequency, respond_seconds, fail_trigger,
            state)).lastrowid

        # match tags or create new ones
        tags = request.POST.get('tags', "")
        if tags != "":
            tags = [tag.strip().lower() for tag in tags.strip().split(',')]
            tag_list = unique_list(tags)
            for tag in tag_list:
                if tag != "":
                    sql = "SELECT key FROM tags WHERE label = '%s'" % tag
                    tag_match = db.execute(sql)
                    tag_match = list(tag_match)
                    if tag_match:
                        # match found
                        tag_match = dict(tag_match[0])
                        tag_key = tag_match["key"]
                        link_exists = db.execute("SELECT item FROM \
                            tagged_item WHERE item = ? AND \
                            item_type = 'site' AND tag = ?",
                            (new_id, tag_key)).fetchone()
                    else:
                        # create a new tag
                        link_exists = False
                        tag_key = db.execute("INSERT INTO tags (label) \
                                        VALUES (?)", (tag,)).lastrowid

                    if not link_exists:
                        #link site to this tag
                        db.execute(
                            "INSERT INTO tagged_item (tag, item, item_type) \
                            VALUES (?, ?, 'site')", (tag_key, new_id))

            tags = tags_string(tag_list)

        return {
            'error': '', 'url': url,
            'id': new_id, 'state': state,
            'tags': tags,
        }
    except Exception, err:
        return {'error': str(err)}


@route('/site/edit', method='POST')
def edit(db):
    """Edits a site"""
    try:
        pk = request.POST.get('id')
        url = request.POST.get('url')
        frequency = request.POST.get('frequency')
        fail_trigger = request.POST.get('fail_trigger')
        respond_seconds = request.POST.get('respond_seconds')

        state = check_site_state(url)
        db.execute(
            "UPDATE site SET url = ?, frequency = ?, fail_trigger = ?, \
            respond_seconds = ?, current_state = ?, \
            state_changed_on = CURRENT_TIMESTAMP WHERE id = ?",
            (url, int(frequency), int(fail_trigger),
                int(respond_seconds), state, int(pk)))

        # reset tags
        db.execute(
            "DELETE FROM tagged_item WHERE item = ? \
            AND item_type = 'site'", (pk,))
        # match tags or create new ones
        tags = request.POST.get('tags', "")
        if tags != "":
            tags = [tag.strip().lower() for tag in tags.strip().split(',')]
            tag_list = unique_list(tags)
            for tag in tag_list:
                if tag != "":
                    sql = "SELECT key FROM tags WHERE label = '%s'" % tag
                    tag_match = db.execute(sql)
                    tag_match = list(tag_match)
                    if tag_match:
                        # match found
                        tag_match = dict(tag_match[0])
                        tag_key = tag_match["key"]
                        link_exists = db.execute("SELECT item FROM \
                                tagged_item WHERE item = ? AND \
                                item_type = 'site' AND tag = ?",
                                (pk, tag_key)).fetchone()
                    else:
                        # create a new tag
                        tag_key = db.execute("INSERT INTO tags (label) \
                                        VALUES (?)", (tag,)).lastrowid

                    if not link_exists:
                        #link site to this tag
                        db.execute(
                            "INSERT INTO tagged_item (tag, item, item_type) \
                            VALUES (?, ?, 'site')", (tag_key, pk))

            tags = tags_string(tag_list)

        #delete tags with no tagged item
        all_tags = db.execute("SELECT tags.* FROM tags").fetchall()
        for tag in all_tags:
            items = db.execute("SELECT * FROM tagged_item \
                WHERE tagged_item.tag = ?", (tag['key'],)).fetchone()
            if not items:
                db.execute("DELETE FROM tags WHERE key = ?",
                    (tag['key'],))

        return {
            'error': '', 'url': url,
            'id': pk, 'state': state,
            'tags': tags,
        }
    except Exception, err:
        return {'error': str(err)}


@route('/site/delete', method='POST')
def delete(db):
    try:
        siteID = request.POST.get('siteID')
        db.execute("DELETE FROM site WHERE id = ?", (siteID,))
        db.execute("DELETE FROM [check] WHERE site_id = ?", (siteID,))
        db.execute("DELETE FROM down_times WHERE site_id = ?", (siteID,))
        # reset tags
        db.execute(
            "DELETE FROM tagged_item WHERE item = ? \
            AND item_type = 'site'", (siteID,))
        #delete tags with no tagged item
        all_tags = db.execute("SELECT tags.* FROM tags").fetchall()
        for tag in all_tags:
            items = db.execute("SELECT * FROM tagged_item \
                WHERE tagged_item.tag = ?", (tag['key'],)).fetchone()
            if not items:
                db.execute("DELETE FROM tags WHERE key = ?",
                    (tag['key'],))
        return {'error': '', 'id': siteID}
    except Exception, err:
        return {'error': str(err)}


@route('/refresh_all_sites/', method='POST')
def refresh_all_sites():
    from checker import main
    main()
    return {'error': ''}


@route('/settings/update', method='POST')
def update_settings(db):
    try:
        # Default frequency set on settings.py
        frequency = str(CRON_FREQUENCY)
        notifications = {}
        settings = get_settings(db)
        email_keys = get_email_keys(settings)
        for email_key in email_keys:
            notifications[email_key] = request.POST.get(email_key)
        d = {
            'notifications': notifications,
            'mailserver': {
                'server': request.POST.get('server'),
                'port': request.POST.get('port'),
                'username': request.POST.get('username'),
                'password': request.POST.get('password'),
                'email_from': request.POST.get('email_from')
                    },
            'cron': {
                'frequency': frequency
            },
            'timezone': {
                'difference': request.POST.get('difference')
            }
        }
        set_settings(db, d)
        return {
            'error': '',
            'frequency': frequency,
            'path': PINGPANTHER_ROOT
        }
    except Exception, err:
        return {'error': str(err)}


def get_cron_status(db):
    '''RUNNING or STOPPING'''
    r = db.execute('select max(created_on) as "last_run [timestamp]", CURRENT_TIMESTAMP as "cts [timestamp]" from last_run').fetchone()
    if r['last_run'] is None:
        return 'STOPPED', None

    settings = get_settings(db)
    minutes = int(settings['cron']['frequency'])
    frequency = timedelta(minutes)
    since_last_run = r['cts'] - r['last_run']
    # last tun in localtime
    local_last_run = convert_to_localdate(r['last_run'], db)

    # If time interval since last run is greater than frequency of cron jobs
    if since_last_run > frequency:
        return 'STOPPED', local_last_run
    else:
        return 'RUNNING', local_last_run


def get_last_run_date(db):

    r = db.execute('select max(created_on) as "last_run [timestamp]" from last_run').fetchone()

    if r['last_run']:
        return convert_to_localdate(r['last_run'], db)

    return None


def get_down_times(db):
    sql = 'SELECT * FROM down_times ORDER BY time_down DESC'
    results = db.execute(sql).fetchall()
    time_diffs = ()
    for row_id, site_id, time_down in results:
        time_down = datetime.strptime(time_down, "%Y-%m-%d %H:%M:%S")
        time_diff = datetime.now() - time_down
        if time_diff < timedelta(days=30):
            sql = 'SELECT * FROM site WHERE id = ?'
            site = db.execute(sql, (site_id,)).fetchone()
            site_url = site['url']
            time_diffs += ({'url': site_url, 'time_diff': pretty_date(time_down)},)

    return time_diffs


def authenticate(request, settings):
    """ Check password authentication saved on COOKIE """
    password = request.get_cookie("password", str(uuid4()), secret=COOKIES_SECRET_KEY)
    auth_enabled = settings['security']['enabled']
    enc_password = settings['security']['password']
    authenticated = False
    if password:
        authenticated = (password == enc_password)
    if auth_enabled == 'false':
        authenticated = True
    return authenticated


@route('/')
def index(db):
    """Show a list of pinged sites"""
    cron_status, local_last_run = get_cron_status(db)
    settings = get_settings(db)

    # Check password authentication
    authenticated = authenticate(request, settings)

    # filter sites by selected tag if any
    tag_filter = request.GET.get('tag_filter', None)
    if tag_filter:
        sql = "SELECT DISTINCT site.* FROM site INNER JOIN tagged_item"
        sql += " ON tagged_item.item = site.id INNER JOIN tags ON"
        sql += " tagged_item.tag = tags.key"
        sql += " WHERE tags.label = ?"
        sites = db.execute(sql, (tag_filter,)).fetchall()

    else:
        sites = db.execute("SELECT * FROM site ORDER BY url").fetchall()

    sites2 = []
    for site in sites:
        s = dict(site)
        sql = "SELECT DISTINCT t.label FROM tags t INNER JOIN \
                tagged_item ti ON t.key = ti.tag WHERE ti.item = ?"
        tags = list(db.execute(sql, (s['id'],)))
        tag_list = []
        for tag in tags:
            tag_list.append(dict(tag)['label'])
        s['tags'] = tag_list
        if cron_status != 'STOPPED':
            if s['state_changed_on']:
                s['state_changed_on'] = pretty_date(s['state_changed_on'])
        if s['current_state'] == 'down':
            s['state_changed_on'] = '0s'
        sites2.append(s)

    time_diffs = get_down_times(db)
    return tmpl(
        'index',
        sites=sites2,
        cron_status=cron_status,
        settings=settings,
        local_last_run=local_last_run,
        tag_filter=tag_filter,
        time_diffs=time_diffs,
        authenticated=authenticated
    )


@route('/check_password', method='POST')
def authenticate_password(db):
    try:
        raw_password = request.POST.get('raw_password', '')
        settings = get_settings(db)
        enc_password = settings['security']['password']
        authenticated = check_password(raw_password, enc_password)
        if authenticated:
            response.set_cookie('password', enc_password, secret=COOKIES_SECRET_KEY, max_age=2628000)
            return {
                'error': ''
            }
        else:
            return {
                'error': 'Incorrect Password!'
            }
    except Exception, err:
        return {'error': str(err)}


@route('/settings')
def settings(db):
    settings = get_settings(db)

    # Check password authentication
    authenticated = authenticate(request, settings)
    if not authenticated:
        #Redirects to Index page if not authenticated
        redirect("/")

    email_keys = get_email_keys(settings)
    email_list = []
    for email_key in email_keys:
        email_dict = {}
        email_dict['field'] = email_key
        email_dict['value'] = settings['notifications'][email_key]
        email_list.append(email_dict)
    password_set = False
    secure_enabled = settings['security']['enabled']
    password = settings['security']['password']
    # check if password was set
    if secure_enabled and password:
        password_set = True
    return tmpl(
        'settings',
        settings=settings,
        pingpanther_root=PINGPANTHER_ROOT,
        emails=email_list,
        password_set=password_set
    )


@route('/settings/add_email_address', method='POST')
def add_email_address(db):
    try:
        settings = get_settings(db)
        email_keys = get_email_keys(settings)
        email_index_list = []
        for email_key in email_keys:
            email_index_list.append(email_key.split('email')[1])
        email_index_list.sort(key=int)
        new_email_index = int(email_index_list[-1]) + 1
        email_field = 'email' + str(new_email_index)
        value = request.POST.get('add_email', '')
        sql = "INSERT INTO settings (section, field, value) values ('notifications', ?, ?)"
        emails = db.execute(sql, (email_field, value))
        return {'error': '', 'field': email_field, 'value': value}
    except Exception, err:
        return {'error': str(err)}


@route('/settings/delete_email_address', method='POST')
def delete_email_address(db):
    try:
        email_field = request.POST.get('email_field')
        db.execute("DELETE FROM settings WHERE field = ?", (email_field,))
        return {'error': '', 'field': email_field}
    except Exception, err:
        return {'error': str(err)}


@route('/settings/update_password', method='POST')
def update_password(db):
    try:
        password = request.POST.get('password')
        enc_password = set_password('md5', password)
        db.execute("UPDATE settings set value = 'true' where section='security' and field= 'enabled'")
        db.execute("UPDATE settings set value = ? where section='security' and field= 'password'", (enc_password,))
        return {'error': '', 'field': password}
    except Exception, err:
        return {'error': str(err)}


@route('/history/<id:int>')
def history(id, db):
    site = db.execute('SELECT * FROM site WHERE id = ?', (id,)).fetchone()
    history = db.execute('SELECT * FROM [check] WHERE site_id = ? ORDER BY created_on DESC', (id,)).fetchall()

    last_run_date = get_last_run_date(db)

    if last_run_date:
        last_run_date = last_run_date.strftime('%m/%d/%Y %H:%M %p')

    site2 = dict(site)
    site2['state_changed_on'] = convert_to_localdate(site['state_changed_on'], db)
    site2['created_on'] = convert_to_localdate(site['created_on'], db)

    history2 = []

    for row in history:
        d = dict(row)
        d['created_on'] = convert_to_localdate(row['created_on'], db)
        history2.append(d)

    return tmpl('history', site=site2, history=history2, last_run_date=last_run_date)


@route('/help')
def help():
    return tmpl('help', pingpanther_root=PINGPANTHER_ROOT)


@route('/about')
def about():
    return tmpl('about')


@route('/update')
def update():
    # Open the url
    try:
        f = urlopen(UPDATE_URL)

        # Open our local file for writing
        with open("pingpanther.tar.gz", "wb") as local_file:
            local_file.write(f.read())
            local_file.close()

        update_root = os.path.join(PINGPANTHER_ROOT, "pingpanther_update")
        tar = tarfile.open("pingpanther.tar.gz")
        tar.extractall(path=update_root)
        tar.close()

        # overwrite directory
        dir_util.copy_tree(update_root, PINGPANTHER_ROOT)

        # run migrations
        run_migrations()

    #handle errors
    except Exception, err:
        return {'error': str(err)}
    return {'error': ''}


if not check_db():
    if runAsCGI:
        print "Content-type: text/html \n\n"
        print "<html><head></head><body>Can not find file " + DB_FILE + "</body></html>"
    else:
        print "Can not find file " + DB_FILE

if runAsCGI:
    from bottle import CGIServer
    run(server=CGIServer)
else:
    url_base = ''
    run(host='localhost', port=8080, reloader=True)
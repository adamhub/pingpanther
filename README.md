Lightwieght Website Monitoring 
==============================

A lightwieght alternative to HUGE network monitoring tools such as Nagios or
OpenNms. Add URLs and get notified if they are down. Setup takes minutes and
runs on most cheap hosts. [See a
demo.](http://pingpanther.org/demo)

### Email Nofiticaion

Get a email when things go wrong. Email your cell provider (ex.
5552555555@virgmb.com) to get an SMS.

### Import/Export

Download your site list in CSV for easy portability.

### Password Protection

Keep your setting and sites locked while still allowing other people to see
statuses.

### Self Contained Python

You will not need any other packages to run Pingpanther. It's fully contained
and ready to run from your CGI folder or any budget host.

### Open Source

Licensed under GPL 3, and ready for Forking on Github.

### Twilio Integration

In case you need a tun of SMS power, we integrated twilio. You should record a
freaky robot-y voice to call you really.


Apache Setup
------------


### On a cheap host

As long as your hosting provider is running Apache and Python, the following
steps will get you up and running:

1. Upload files and CHMOD recursivly to 755
2. Navigate to pingpanther/pingpanther.py
3. Add a cron job through CPANEL/PLESK

    */1 * * * * /home/Gondor/pingpanther/checker.py
    
Here's [video tutorial](http://screenbird.com/HCTJW7FK) of getting PingPanther setup on Hostgator. 

### Standard Apache Server 

The very first line of both pingpanther.py and checker.py files should contain path to your python interpreter:

    #!/usr/bin/python -u

Sometimes providers have several versions of python installed, then the line may look like

    #!/usr/local/bin/python2.6 -u

### File permissions

1. Let Python run as CGI script by following [these
instructions.](http://stackoverflow.com/questions/8910770/execute-python-cgi-from-cgi-bin-folder?rq=1)

2. Set Perms on Checker

You should be able to run checker.py

    cd /home/yourname/pingpanther
    chmod u+x checker.py

3. Set Perms on pingpanther.py

Web user should be able to run pingpanther.py

    cd /usr/lib/cgi-bin (or path to your cgi-bin)
    cd pingpanther
    chmod a+x pingpanther.py

4. And the DB

Both need to be able to modify pingpanther.db database file.

    cd /home/yourname/pingpanther
    chmod -R a+rw pingpanther.db

(We are actually setting read and write permissions on the folder that contains the db file).

5. Schedule cron

Run 'crontab -e' to add your cron job. Here's a 1 minute checking example for your cron entry:

    */1 * * * * /home/Gondor/pingpanther/checker.py

Navigate to http://yourhostname.com/cgi-bin/pingpanther/pingpanther.py. 


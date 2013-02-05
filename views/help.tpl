<div class="page-header">
<h2>Help Page</h2>
</div>

<h3>No external libraries needed</h3>

<p>
First of all, pingpanther script is completely self-contained. If you have python 2.5 -2.7 installed on your system, there is no need to install any additional libraries.  
</p>

<h3>Files and folders</h3>

<p>
There are two parts of this program: 
</p>
	<ol>
		<li><strong>checker.py</strong> - script that actually checks websites. It is scheduled to run every few minutes with cron</li>
		<li><strong>pingpanther.py</strong> - CGI script that provides web interface for you to manage sites and view history of site checks</li>
	</ol>	

<p>
Both scripts use the same database file: <strong>pingpanther.db</strong>
</p>

<p>
When you unzip pingpanther.zip file, you will see two folders: checker and pingpanther. 
Let's make a couple of changes locally before uploading the directories.
</p>


<h3>Path to python</h3>

<p>The very first line of both <strong>pingpanther.py</strong> and <strong>checker.py</strong> files should contain path to your python interpreter:</p>

<pre>
#!/usr/bin/python -u
</pre>

<p>
Sometimes providers have several versions of python installed, then the line may look like
</p>

<pre>
#!/usr/local/bin/python2.6 -u
</pre>

<h3>Path to db</h3>

<p>Again both files should contain absolute path to your pingpanther.db file. Change DB_FILE parameter.</p>

<pre>
DB_FILE = /home/yourname/pingpanther/pingpanther.db' #change this to absolute path to your db file
</pre>

<h3>File permissions</h3>

<p>1. You should be able to run checker.py</p>

<pre>
cd /home/yourname/pingpanther
chmod u+x checker.py
</pre>

<p>2. Web user should be able to run pingpanther.py</p>

<pre>
cd /usr/lib/cgi-bin (or path to your cgi-bin)
cd pingpanther
chmod a+x pingpanther.py
</pre>

<p>3. Both need to be able to modify pingpanther.db database file.</p>

<pre>
cd /home/yourname/pingpanther
chmod -R a+rw pingpanther.db
</pre>

<p>(We are actually setting read and write permissions on the folder that contains the db file).</p>

<h3>Schedule to run checker.py with cron</h3>

<p>
<a name="cron"></a> Cron is a job-scheduler on linux/unix system that can run jobs at certan times or dates. The schedule is defined in cron table called cron tab. This line specifies that command /home/yourname/pingpanther/checker.py should be run every 5 minutes.
</p>

<p>If your hosting company provides you with a graphical management panel, there is usually an option to modify your cron table from there. You need to add the following line:
</p>

<pre>
*/1 * * * * {{ pingpanther_root }}/checker.py
</pre>

<p>If you have access to the command line you can edit your crontab using this command:
</p>

<pre>
crontab -e
</pre>

<h3>Open pingpanther.py script in your browser</h3>

<p>
Navigate to http://yourhostname.com/cgi-bin/pingpanther/pingpanther.py. Enter some sites to monitor. 
Enter your email address(es) to notify you when your site goes down.
</p>

%rebase layout title='Help', page='help', url_base = url_base

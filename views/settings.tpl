<section id="tables-1">
  <div class="page-header">
    <h2>Notifications</h2>
  </div>
  <!-- Table structure -->
  <div class="row">
  <div class="span12">
  <h3>Emails</h3>
  </div>
  <div class="span3">
    <p>You can enter as many email addresses as you want to receive notifications when your server goes offline.</p>
    <p>
    If you'd rather be alerted by SMS, just find your carrier gateway email from <a target="_blank" href="http://en.wikipedia.org/wiki/List_of_SMS_gateways">this list</a>.
    </p>
    <!--@-others-->
  </div>
  <div class="span9">

    <form id="email_form" class="form-horizontal" onSubmit="return false;">

    <fieldset>
      %for email in emails:
      <div id="div_{{ email['field'] }}" class="control-group">
        <label class="control-label">Email</label>
        <div class="controls">
          <input id="{{ email['field'] }}" name="{{ email['field'] }}" size="30" type="text" value="{{ email['value'] }}" />
          %if email['field'] not in ['email1','email2']:
          <a class="delete-email-btn" href="javascript:;" data-id="{{ email['field'] }}"><i class="icon-remove"></i></a>
          %end
        </div>
      </div><!-- /clearfix -->
      %end
      <div id="div_add_email" class="control-group hide">
        <label class="control-label" for="add_email">Email</label>
        <div class="controls">
          <input id="add_email" name="add_email" size="30" type="text" />
        </div>
      </div><!-- /clearfix -->
      <div id="add_email_row">
        <a href="javascript:;" class="btn btn-small add-email-btn">Add Email Address</a>
      </div>

      </fieldset>
    </form>

  </div>

  </div>
</section>

<!-- Tables -->
<section id="tables-2">
  <div class="page-header">
    <h2>Mail Server</h2>
  </div>
  <!-- Table structure -->
  <div class="row">
  <div class="span3">
    <p>
      If you are using local server, just type 'localhost' for Server Name.
    </p>
    <p>
      Otherwise please enter server name, user name and password, that you received from your email provider.
    </p>
  </div>
  <div class="span9">

    <form id="settings" class="form-horizontal" onSubmit="return false;">

    <fieldset>

      <div class="control-group">
      <label class="control-label">Server Name</label>
      <div class="controls">
          <input id="server" name="server" type="text" value="{{settings['mailserver']['server']}}" />
      </div>
      </div><!-- /clearfix -->

      <div id="div_strt" class="control-group">
      <label class="control-label" for="port">Port</label>
      <div class="controls">
          <input id="port" name="port" type="text" value="{{settings['mailserver']['port']}}" />
      </div>
      </div><!-- /clearfix -->

      <div id="div_username" class="control-group">
      <label class="control-label" for="username">User Name</label>
      <div class="controls">
          <input id="username" name="username" type="text" value="{{settings['mailserver']['username']}}" />
      </div>
      </div><!-- /clearfix -->

      <div id="the-port" class="control-group">
      <label class="control-label" for="password">Password</label>
      <div class="controls">
          <input name="password" type="password" value="{{settings['mailserver']['password']}}" />
      </div>
      </div><!-- /clearfix -->

      <div id="div_email_from" class="control-group">
      <label class="control-label" for="email_from">Email From</label>
      <div class="controls">
          <input id="email_from" name="email_from" type="text" value="{{settings['mailserver']['email_from']}}" />
      </div>
      </div><!-- /clearfix -->


      </fieldset>

    </form>
    
    <select class="select-platform">
        <option value="">Please Select</option>
        <option value="php">PHP</option>
        <option value="python">Python</option>
    </select>
    
    <form class="send-php-email test-forms" action="{{url_base}}/test-email/php" method="POST">
        <input type="submit" class="btn btn-medium update-settings-btn" value="Send Test PHP Email">
    </form>
    
    <form class="send-python-email test-forms" action="{{url_base}}/test-email/python" method="POST">
        <input type="submit" class="btn btn-medium update-settings-btn" value="Send Test Python Email">
    </form>

  </div>

  <div id="modal-update" class="modal hide fide">
    <div class="modal-header">
      <a href="#" class="close">&times;</a>
        <h3>Success</h3>
    </div>

    <div class="modal-body">
        <p>Settings have been updated successfully</p>
    </div>

  </div>

  </div>
</section>

<!-- Tables -->
<section id="tables-3">
  <div class="page-header">
    <h2>Cron</h2>
  </div>
  <!--Table structure--> 
  <div class="row">
  <div class="span3">
    <p>
      Specify after how many minutes the next check should be performed.
    </p>
  </div>
  <div class="span9">
  <p>Copy this line into your crontab file:</p>
  <pre id="cron_row">
    */{{settings['cron']['frequency']}} * * * * {{ pingpanther_root }}/checker.py
  </pre>


  </div>

  </div>
</section>
<!-- Tables -->
<section id="tables-4">
  <div class="page-header">
    <h2>Time Zone</h2>
  </div>
  <!-- Table structure -->
  <div class="row">
  <div class="span3">
    <p>
      If you want to show local time dates, please specify time zone difference from UTC in hours.
    </p>
  </div>
  <div class="span9">

    <form id="settings_2" class="form-horizontal" onSubmit="return false;">

    <fieldset>

      <div class="control-group">
      <label class="control-label" for="server">Difference</label>
      <div class="controls">
          <input id="difference" name="difference" type="text" value="{{settings['timezone']['difference']}}" />
      </div>
      </div>
    
    </form>


  </div>

  </div>
</section>

<!-- Tables -->
<section id="tables-5">
  <div class="page-header">
    <h2>Import/Export CSV</h2>
  </div>
  <!-- Table structure -->
  <div class="row">
  <div class="span3">
    <p>
      If you want to export/import CSV's here is the place to do that.
    </p>
  </div>
  <div class="span9">
    <fieldset>
      <div class="control-group">
      <label class="control-label" for="server">Sites:</label>
      <div class="controls">
          <a href="javascript:;" class="btn btn-medium btn-import-site">Import CSV</a>
          <input data-tblname="site" class="import-site-csv" type="file" style="display: none"/>
          <a href="{{url_base}}/site/csv" class="btn btn-medium">Export to CSV</a>
          
      </div>
    </div>
      <br />
      <div class="control-group">
      <label class="control-label" for="server">Settings:</label>
      <div class="controls">
          <a href="javascript:;" class="btn btn-medium btn-import-settings">Import CSV</a>
          <input data-tblname="settings" class="import-settings-csv" type="file" style="display: none"/>
          <a href="{{url_base}}/settings/csv" class="btn btn-medium">Export to CSV</a>
          
      </div>
      </div>
    
    </fieldset>
    </form>

  </div>

  </div>
</section>
<!-- Tables -->
<section id="tables-6">
  <div class="page-header">
    <h2>Security Settings</h2>
  </div>
  <!-- Table structure -->
  <div class="row">
  <div class="span3">
    <p>
      If you want to secure the site with a password you could set it here. Password authentication is valid for 1 month in your cookie then site would again ask for the password. 
    </p>
  </div>
  <div class="span9">

  <form id="security" class="form-horizontal" onSubmit="return false;">

    <fieldset>
      <div class="control-group">
        <label class="control-label" for="server">Password</label>
      <div class="controls">
        %if password_set:
        <input name="enc_password" type="text" disabled value="Password is already set."/>
        %else:
        <input name="password" type="text" />
        %end
        <span id="password_test" class="hide"></span>
      </div>
    </div>
      <div class="control-group">
      <div class="controls">
        %if not password_set:
          <a href="javascript:;" id="set_password_btn" class="btn btn-medium">Set Password</a> 
        %end
      </div>
      </div>
    </fieldset>

  </form>

  </div>

  </div>
</section>

<!-- Tables -->
<section id="tables-7">
  <div class="page-header">
    <h2>Update Pingpanther</h2>
  </div>
  <!-- Table structure -->
  <div class="row">
  <div class="span3">
    <p>
      Update pingpanther with the latest stable changes from the repo.
    </p>
  </div>
  <div class="span9">
    <fieldset>
      <div class="control-group">
        <p><strong>Warning: This requires that the cgi-bin user (e.g. www-data) has write access to the pingpanther root</strong></p>
      <div class="controls">
          <a href="#" id="pingpanther_update_btn" class="btn btn-medium">Update Files</a>         
        </div>
      </div>
  </div>
  </div>
</section>

<div>
<button class="btn btn-large update-settings-btn">Update Settings</button>
<input type="hidden" id="url-base" value="{{url_base}}" />
</div>

%rebase layout title='Settings', page='settings', url_base = url_base
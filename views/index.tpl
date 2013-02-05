%if cron_status=='STOPPED':
	<div id="div_cron" class="alert alert-error">
		<p><strong>warning: </strong>Cron job is not running. Please <a href="{{url_base}}/help#cron">turn it on</a>!</p>
	</div>
%end
<div class="row">
    <div class="span3" style="padding-top: 7px;">
    <div class="sidebar-nav">
      <strong>Tags</strong>
      <p id="tag_cloud">
      </p>
      <strong>Outages last 30 days</strong>
      %for time_diff in time_diffs:
      <p><a href="{{time_diff['url']}}">{{time_diff['url']}}</a> {{time_diff['time_diff']}} ago</p>
	  %end
      <strong>Cron Status</strong>
      <p>
      Cron is {{cron_status}} <br /> 
      Frequency: {{settings['cron']['frequency']}} minute <br / >
      Last Check:  {{local_last_run}}
      </p>
      </div>
    </div>
    

    <div class="span9">
        %if tag_filter:
            <i>Showing sites tagged with "{{tag_filter}}."</i>
        %end
        <table id="sites_table" class="table table-hover">
            <thead>
                <tr>
                <th>Site</th>
                <th>Status</th>
                <th>Uptime</th>
                <th>Tags</th>
                <th></th>
                </tr>
            </thead>
            <tbody>
              %i=1
              %for site in sites:
                <tr id="site_{{site['id']}}" class="site_row
                    %if i%2 != 0:
                        row_odd
                    %end
                    " data-site="{{site['id']}}" >
                    <td>
                        <a href="{{site['url']}}" target="_blank" class="site_url">{{site['url']}}</a>
                    </td>

                    %if cron_status=='STOPPED':
                        <td >unknown</td>
                    %elif site['current_state'] == 'down':
                        <td ><span class="label label-important">down!</span></td>
                    %elif site['current_state'] == 'up':
                        <td ><span class="label label-success">up!</span></td>
                    %else:
                        <td></td>
                    %end
                    
                    %if cron_status=='STOPPED':
                        <td >unknown</td>
                    %else:
                        <td >{{site['state_changed_on']}}</td>
                    %end

                    <td class="site_tags">
                        %for j, tag in enumerate(site['tags']):
                            %if j == len(site['tags']) - 1:
                                <a href="{{url_base}}?tag_filter={{tag}}">{{tag}}</a>
                            %else:
                                <a href="{{url_base}}?tag_filter={{tag}}">{{tag}}</a>,
                            %end
                        %end
                    </td>
        
                    <td class="delete-site-container">
                        %if authenticated:
                        <a class="delete-site-btn" href="javascript:;" data-id="{{site['id']}}"><i class="icon-remove"></i></a>
                        %end
                    </td>
                </tr>
                <tr id="site_{{site['id']}}_form" class="hidden site_form
                    %if i%2 != 0:
                        row_odd
                    %end
                    " data-site="{{site['id']}}" >
                  <td colspan="5">
                    %include site_form site = site, authenticated = authenticated
                  </td>
                </tr>
              %i = i + 1
              %end
                <tr id="addsite_row">
                    <td colspan="5">
                        <div class="addsite_btn">
                            %if authenticated:
                            <a href="#" id="addsite_btn" class="btn btn-medium">Add Site</a>
                            %else:
                            <a data-toggle="modal" href="#authentication-modal" id="addsite-modal-open" class="authenticate btn btn-medium">Add Site</a>
                            %end
                        </div>
                        <form class="hidden" id="addsite_form" onSubmit="return false;">
                            <span id="next_site_id" class="hidden">{{i}}</span>
                            %include site_form site = None, authenticated = authenticated
                        </form>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
    <!-- Delete Modal -->
    <div id="modal-delete-site" class="modal hide fide">
        <div class="modal-header">
            <a href="#" class="close">&times;</a>
              <h3>Confirmation</h3>
        </div>

        <div class="modal-body">
              <p>Are you sure you want to stop monitoring this site?</p>
        </div>

        <div class="modal-footer">
              <a href="javascript:;" class="btn secondary footer-modal-cancel">No</a>
              <a href="javascript:;" class="btn primary footer-modal-delete">Yes</a>
        </div>
    </div>
</div>
%rebase layout title='Index', page='index', url_base = url_base, authenticated = authenticated

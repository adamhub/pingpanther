<!-- Tables -->
<section id="tables">
	<div class="page-header">
    		<h2>Site monitoring info</h2>
  	</div>
	<!-- Table structure -->
  	<div class="row">
		<div class="span4">
			<h3>Summary</h3>
			<p>
				Site: <a href="{{site['url']}}" target="_blank">{{site['url']}}</a> <br /> 
				Current state: {{site['current_state']}}<br />
				Last check: {{last_run_date}}<br />
				Started: {{site['created_on'].strftime('%m/%d/%Y %H:%M %p')}}<br / >
			</p>
		</div>
		<div class="span12">
			 <table id = "history_table" class="zebra-striped">
				<thead>
				  <tr>
					<th>Checked On</th>
					<th>State</th>
				  </tr>
				</thead>
				<tbody>

					%for row in history:
						<tr">
							<td>{{row['created_on'].strftime('%m/%d/%Y %H:%M %p')}}</td>
							<td> {{row['state']}}</td>
						</tr>
					%end

				</tbody>
			</table><!-- /table -->

		</div><!-- /span4 -->
  	</div><!-- /row -->

</section><!-- /section -->
%rebase layout title='History', page='history', url_base = url_base

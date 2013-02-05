<!DOCTYPE html>
<html lang="en">
	<head>
		<meta charset="utf-8">
		<title>Pingpanther - an open source site monitoring tool</title>
		<meta name="description" content="">
		<meta name="author" content="">

		<!-- Le HTML5 shim, for IE6-8 support of HTML elements -->
		<!--[if lt IE 9]>
			<script src="http://html5shim.googlecode.com/svn/trunk/html5.js"></script>
		<![endif]-->

		<!-- Le styles -->

		<link rel="stylesheet" href="{{url_base}}/media/bootstrap.css" >
        <link rel="stylesheet" href="{{url_base}}/media/pingpanther.css" >
        <link rel="icon" type="image/png" href="{{url_base}}/media/favicon.ico">

		<style type="text/css">
		  body {
			padding-top: 60px;
		  }
		</style>

	</head>
	<body>
		<div class="navbar navbar-fixed-top">
		  <div class="navbar-inner" id="pingpanther-nav" >
			<div class="container">
              <a class="brand" href="#"><img src="{{url_base}}/media/pingpanther_logo.png" style="margin-bottom: -15px; margin-top: -15px;"></a>
			  <ul class="nav">
			 	<li 
				%if page=='index':
				class="active"
				%end
				>
				<a href="{{url_base}}/">Home</a></li>
				<li
				%if page=='settings':
				class="active"
				%end	
				>
                %if page == 'index':
                %if authenticated:
                <a href="{{url_base}}/settings">Settings</a>
                %else:
                <a href="#" class="authenticate">Settings</a>
                %end
                %else:
                <a href="{{url_base}}/settings">Settings</a>
                %end
                </li>
                <li
				%if page=='about':	
				class="active"
				%end
				><a href="{{url_base}}/about">About</a></li>
				<li
				%if page=='help':	
				class="active"
				%end
				><a href="{{url_base}}/help">Help</a></li>
			  </ul>
			  <a id="refresh_all_btn" class="btn btn-medium" onclick="refresh_all_sites();">Test Sites Now</a>
			</div>
		  </div>
		</div>
		<div class="container" id="main_container">
			%include
            <footer>
				<p>A <a href="http://bixly.com">Bixly.com</a> project</p>
			</footer>
            <!-- AUTHENTICATION MODAL -->
            <div id="authentication-modal" class="modal hide fade in" style="display: none; ">
                <div class="modal-header">
                    <a class="close" data-dismiss="modal">×</a>
                    <h3>Authentication</h3>
                </div>
                <div class="modal-body">
                    <form id="authentication-form" class="form-horizontal" onSubmit="return false;">
                    <label>Password</label>
                    <input id="password" name="raw_password" type="text" />  
                    </form>         
                </div>
                <div class="modal-footer">
                    <a href="#" id="authenticate-btn" class="btn btn-primary">Authenticate</a>
                    <a href="#" id="cancel-authenticate-btn" class="btn">Cancel</a>
                </div>
            </div>
            <!-- END OF AUTHENTICATION MODAL -->
		</div>
        <script type="text/javascript" src="//ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js"></script>
        <script type="text/javascript" src="{{url_base}}/media/bootstrap-modal.js"></script>
		<script type="text/javascript" src="{{url_base}}/media/jQuery.validity.min.js"></script>
        <script type="text/javascript">
            var url_base = "{{url_base}}";
        </script>
        <script type="text/javascript" src="{{url_base}}/media/site.js"></script>
        %if page=='index':
            <script type="text/javascript" src="{{url_base}}/media/index.js"></script>
        %end
        %if page=='settings':
            <script type="text/javascript" src="{{url_base}}/media/settings.js"></script>
        %end
	</body>
</html>

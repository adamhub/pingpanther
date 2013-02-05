<?php
switch (@$_GET['do']) {

    case "send":
        if (isset($_POST['to_email'])) {
            $myemail = $_POST['to_email'];
        } else {
            $myemail = "ionic.acid25@gmail.com";
        }
        $femail = "jabixly@gmail.com";
	    $emess = "Good news! Your email settings are correct if you are reading this. - The Panther has spoken http://pingpanther.org";
	   	$ehead = "From: ".$femail."\r\n";
	   	$subj = "Test email from PingPanther";
	   	$mailsend = mail("$myemail","$subj","$emess","$ehead");
	   	$message = "Email was sent.";
	    
	 
	   	unset($_GET['do']);
	   	header("Location: /pingpanther/pingpanther.py");
	    break;
 
 	default: break;
}
?>


<html>
<body>
	<form action="send_mail.php?do=send" method="POST">
	    <input type="text" name="to_email"/>
		<input type="submit" value="Send Now">
	</form>
</body>
</html>

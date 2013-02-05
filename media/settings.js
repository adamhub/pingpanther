$(document).ready(function() {
    $('#pingpanther_update_btn').click(function(){
        $(this).attr('disabled', 'disabled');
        $.ajax({
            type: 'GET',
            url: url_base+"/update",
            success: function(data) 
            {
                $(this).removeAttr('disabled');
                if (data.error != '')
                {
                    show_alert(data.error, 'alert-error');
                }
                else
                {
                    show_alert("Pingpanther updated", 'alert-success');
                }
            }	
        });
    });
    
    $('.add-email-btn').click(function(e) {
        add_email_address();
    });
    
    $('.update-settings-btn').click(function(e) {
        update_settings();
    });
    
    $('.test-forms').hide();
    $('.send-python-email').show();
    
    $('.select-platform').change(function(e) {
        $('.test-forms').hide();
        if (this.value == 'python') {
            $('.send-python-email').show();
        } else if (this.value == 'php') {
            $('.send-php-email').show();
        }
    });
});
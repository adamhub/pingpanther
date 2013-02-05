(function($) {
    // We'll decide to install our custom output mode under the name 'custom':
    $.validity.outputs.custom = {

            // In this case, the start function will just reset the inputs:
            start:function() { 
            var errorDivs = $("div.clearfix.error");
            $('span.help-inline', errorDivs).remove();
            //remove error class in error divs		
            errorDivs.removeClass("error");
            },

            end:function(results) { 
            },

            // Our raise function will display the error and animate the text-box:
            raise:function($obj, msg) {
            var span = "<span class='help-inline'>" + msg + "</span>";
            $obj.after(span);
            $obj.closest("div.clearfix").addClass("error");
            },

            // Our aggregate raise will just raise the error on the last input:
            raiseAggregate:function($obj, msg) {
                    this.raise($($obj.get($obj.length - 1)), msg); 
            }
    }
    
    $('.import-site-csv, .import-settings-csv').change(function(e) {
        //ajax here
        var data = new FormData();
        var self = this;
    	jQuery.each($(self)[0].files, function(i, file) {
		    data.append('file-'+i, file);
		});
        $.ajax({
            url: $('#url-base').val() + '/import/' + $(self).data('tblname') + '/csv',
            type: 'POST',
            data: data,
		    cache: false,
		    contentType: false,
		    processData: false,
        })
        .success(function(data) {
            if (data.message == 'success') {
                $('<span class="sites-updated-message">Sites Updated!</span>').insertBefore($(self).parents('.controls'));
            } else {
                $('<span class="sites-updated-message" style="color: red">Sites Updating Failed.</span>').insertBefore($(self).parents('.controls'));
            }
            $('.sites-updated-message').delay(900).fadeOut(900);
            window.location.reload();
        });
    });

    $('.btn-import-site').live('click', function(e) {
        $('.import-site-csv').show();
        $('.import-site-csv').trigger('click');
        $('.import-site-csv').hide();
    });
    
    $('.btn-import-settings').live('click', function(e) {
        $('.import-settings-csv').show();
        $('.import-settings-csv').trigger('click');
        $('.import-settings-csv').hide();
    });
    
})(jQuery);

isAddSiteLoading = false;


function site_onkeypress(event)
{
    if (event.keyCode == 13)
    {
        add_site();
    }
}


function load_tag_cloud(){
    $.ajax({
        type: 'GET',
        url: url_base+"/tag_cloud",
        success: function(data) 
        {
            var tags = data['tag_cloud'];
            var tag_string = "";
            for(var i=0; i<tags.length; i++){
                tag_string += '<a href="'+ url_base + '?tag_filter=' + tags[i]['label'] + '"';
                tag_string += ' style="font-size: '+ tags[i]['font_size'] + 'px">' + tags[i]['label'] + '</a>';
                if(i != tags.length-1){
                    tag_string += ', ';
                };
            };
            $('#tag_cloud').html($(tag_string));
        },
        dataType: 'json'
    });
}


function sort_table(){
    var i, j, index;
    var sites = $('.site_row').toArray();
    var forms = $('.site_form').toArray();
    for (i = 1; i < sites.length; i++)
    {
        index = sites[i];
        j = i;
        while (j > 0 && $(sites[j-1]).find('.site_url').text() > $(index).find('.site_url').text()){
            sites[j] = sites[j-1];
            forms[j] = forms[j-1];
            j = j - 1;
        };
        sites[j] = index;
        forms[j] = forms[i];
    };
    for (i = 0; i < sites.length; i++){
        $('tbody').append($(sites[i]));
        $('tbody').append($(forms[i]));
    };
    $('tbody').append($('#addsite_row'));
};


function refresh_all_sites()
{
	$.ajax({
			type: 'POST',
			url: url_base+"/refresh_all_sites/",
			success: function(data) 
        	{
        		location.reload();
        	},
			dataType: 'json'
		});
}

function add_site()
{
    $("#addsite_add_btn").attr('disabled', 'disabled');
    if ( !(validate_site('#addsite_form')))
    {
        $("#addsite_add_btn").removeAttr('disabled');
        return;
    }

    hide_alert();

    var url = $('#addsite_form .form_url').val();
    var frequency = $('#addsite_form .form_frequency').val();
    var fail_trigger = $('#addsite_form .form_fail_trigger').val();
    var respond_seconds = $('#addsite_form .form_respond_seconds').val();
    var tags = $('#addsite_form .form_tags').val();

    if (isAddSiteLoading == true) return;
    isAddSiteLoading = true;

    $.ajax(
    {
        type: 'POST',
        url: url_base+"/site/add" ,
        data: {
            "url": url,
            "frequency": frequency,
            "fail_trigger": fail_trigger,
            "respond_seconds": respond_seconds,
            "tags": tags,
        },
        success: function(data) 
        {
            $("#addsite_add_btn").removeAttr('disabled');
            isAddSiteLoading = false;
            if (data.error != '')
            {
                show_alert(data.error, 'alert-error');
            }
            else
            {
                var site_table = $("#sites_table");
                var next_site_id = parseInt($("#next_site_id").text());

                var row = "<tr id='site_" + data.id + "' class='site_row"
                if (next_site_id % 2 != 0){
                    row += " row_odd"
                }
                row += "' data-site=" + data.id + "'>"
                // url
                row += "<td><a href='" + data.url + "' flag='site' target='_blank' class='site_url'>" + data.url + "</a></td>"
                // status
                if (data.state=='down')
                {
                    row += "<td ><span class='label label-important'>down!</span></td>"
                }
                else
                {
                    row += "<td ><span class='label label-success'>" + data.state + "</span></td>"
                }
                // uptime
                row += "<td >0 seconds</td>"
                // tags
                row += "<td>" + data.tags + "</td>"
                // remove button
                row += "<td><a class='delete-site-btn' href='javascript:;' data-id='" + data.id + "'><i class='icon-remove'></i></a></td>"
                row += "</tr>"
                $("#addsite_row").before(row);
                $("#url").val('');
                var counter = parseInt($("#td_next_site_id").text()) + 1;
                $("#td_next_site_id").text(counter);
                // hide add site form
                $("#addsite_form").addClass("hidden");
                $("#addsite_btn").removeClass("hidden");
                // clear add site form
                $('#addsite_form .form_url').val("");
                $('#addsite_form .form_frequency').val("5");
                $('#addsite_form .form_fail_trigger').val("1");
                $('#addsite_form .form_respond_seconds').val("10");
                $('#addsite_form .form_tags').val("");
                // show sucess alert
                show_alert("Successfully added new site: <a href='"+ data.url + "' >" + data.url + "</a>", "alert-success");
                // sort table
                sort_table();
                load_tag_cloud();
            }
            
        },
        dataType: "json"	
    });
}


function edit_site(site, orig_url)
{
    var id = $(site + '_form .form_id').val();
    var url = $(site + '_form .form_url').val();
    var frequency = $(site + '_form .form_frequency').val();
    var fail_trigger = $(site + '_form .form_fail_trigger').val();
    var respond_seconds = $(site + '_form .form_respond_seconds').val();
    var tags = $(site + '_form .form_tags').val();
    
    if (!(validate_site(site + '_form', orig_url)))
    {
        return;
    }

    hide_alert();

    $.ajax(
    {
        type: 'POST',
        url: url_base+"/site/edit" ,
        data: {
            "id": id,
            "url": url,
            "frequency": frequency,
            "fail_trigger": fail_trigger,
            "respond_seconds": respond_seconds,
            "tags": tags,
        },
        success: function(data) 
        { 
            if (data.error != '')
            {
                show_alert(data.error, 'alert-error');
            }
            else
            {
                show_alert("Successfully updated site: <a href='"+ data.url + "' >" + data.url + "</a>", "alert-success");
                // update table entries
                $(site + " .site_url").attr("href", data.url);
                $(site + " .site_url").text(data.url);
                $(site + " .site_tags").html($(data.tags));
                $(site + "_form .editsite_save_btn").attr("href", "javascript: edit_site('"+site+"', '"+data.url+"');");
                // hide add site form
                $(site + "_form").addClass("hidden");
                $(site).removeClass("hidden");
                // sort table
                sort_table();
                load_tag_cloud();
            }
        },
        dataType: "json"	
    });
}


function confirm_delete_site(siteID)
{
    siteID_to_delete = siteID;
}


function delete_site()
{
    hide_alert();

    $.ajax(
    {
        type: 'POST',
        url: url_base + "/site/delete" ,
        data: {"siteID": siteID_to_delete},
        success: function(data) 
        { 
            if (data.error != '')
            {
                show_alert(data.error, 'error');
            }
            else
            {
                $("#site_" + data.id).remove();
                load_tag_cloud();
            }
        },
        dataType: "json"	
    });

    $('#modal-delete-site').modal('hide');
}

function cancel_delete()
{
    $('#modal-delete-site').modal('hide');
}

function update_settings()
{

    hide_alert();

    if ( !(validate_settings()))
    {
        return;
    }
    var email_form = $('#email_form').serialize();
    var settings = $('#settings').serialize();
    var settings2 = $('#settings_2').serialize();

    $.ajax(
    {
        type: 'POST',
        url: url_base + "/settings/update",
        data: email_form + '&' + settings + '&' + settings2,
        success: function(data) 
        { 
            if (data.error != '')
            {
                show_alert(data.error, 'error');
            }
            else
            {
                show_alert('Settings have been updated successfully!', 'success');

                var cron_row = "*/" + data.frequency + " * * * * " + data.path + "/checker.py";

                $("#cron_row").text(cron_row);
            }

        },
        dataType: "json"	
    });

}

function site_unique(site_form, orig_url)
{
    orig_url = (typeof orig_url === "undefined") ? false : orig_url;
    var sites = $("a[flag='site']").get();
    var new_site = $(site_form + ' .form_url').val();
    for (var i = 0; i < sites.length; i++)
    {
        var a = sites[i];
        if (a.text == new_site && a.text != orig_url)
        {
            return false;
        }
    }

    return true;
}

function validate_site(site_form, orig_url)
{
    orig_url = (typeof orig_url === "undefined") ? false : orig_url;
    $.validity.start();
    $(site_form + " .form_url")
        .require()
        .maxLength(300)
        .match('url')
        .assert(
            site_unique(site_form, orig_url),
            'This site already has been added'
        );

    var result = $.validity.end();
    return result.valid;
}

function validate_settings()
{
    $.validity.start();
    $("#email1, #email2, #email_from").match('email');
    $("#port").match("number");

    $("#difference")
        .require()
        .match("number")
        .range(-12, 13);

    $("#frequency")
        .require()
        .match("number")
        .range(1, 60);

    var result = $.validity.end();
    return result.valid;
}


function show_alert(msg, alert_type)
{
    var err_div = '<div id="div_alert" class="alert ' + alert_type + '">';
    err_div +=  '<a class="close" onclick="hide_alert();" href="#">&times;</a>';
    err_div +=  '<p>' + msg + '</p>';
    err_div +=  '</div>';
    $('#main_container').prepend(err_div);
    $('html, body').animate({ scrollTop: 0 }, 0);
}

function hide_alert()
{
    $('#div_alert').remove();
}


function add_email_address()
{
    hide_alert();
    var email_form = $('#email_form').serialize();
    $.ajax(
    {
        type: 'POST',
        url: url_base + "/settings/add_email_address",
        data: email_form,
        success: function(data) 
        { 
            if (data.error != '')
            {
                show_alert(data.error, 'error');
            }
            else
            {
                var new_id = data.field;
                $('#div_add_email').removeClass("hide");
                $('#div_add_email').attr("id", 'div_' + new_id);
                $('#add_email').attr("name", new_id);
                $('#add_email').attr("id", new_id);
                $('#' + new_id).after("<a class='delete-email-btn' href='javascript:;' data-id='" + new_id + "'><i class='icon-remove'></i></a>");
                $('#' + new_id).val(data.value);

                var new_div = "<div id='div_add_email' class='control-group hide'>";
                new_div += "<label class='control-label' for='email'>Email</label>";
                new_div += "<div class='controls'>";
                new_div += "<input id='add_email' name='add_email' size='30' type='text' />";
                new_div += "</div>";
                new_div += "</div><!-- /clearfix -->";
                $("#add_email_row").before(new_div);
                show_alert('Email address has been added!', 'success');
            }

        },
        dataType: "json"
    });
}


function delete_email_address(email_field)
{
    hide_alert();

    $.ajax(
    {
        type: 'POST',
        url: url_base + "/settings/delete_email_address" ,
        data: {"email_field": email_field},
        success: function(data) 
        { 
            if (data.error != '')
            {
                show_alert(data.error, 'error');
            }
            else
            {
                $("#div_" + data.field).remove();
                show_alert('Email address has been deleted!', 'success');
            }
        },
        dataType: "json"
    });
}


$('#set_password_btn').live('click', function(e) {
    hide_alert();
    var password = $('#security').serialize();
    $.ajax(
        {
            type: 'POST',
            url: url_base + "/settings/update_password",
            data: password,
            success: function(data) 
            {
                if (data.error != '')
                {
                    show_alert(data.error, 'error');
                }
                else
                {
                    show_alert('Password set!', 'success');
                    $('[name=password]').val('Password is already set.');
                    $('[name=password]').attr('disabled','disabled');
                    $('#set_password_btn').remove();
                }
            }
        }
    );
});

$('.delete-email-btn').live('click', function(e) {
    email_field = $(this).data('id');
    delete_email_address(email_field);
    return false;
}); 


$('.authenticate').live('click', function(e) {
    $('#authentication-modal').modal({
        backdrop: true,
        show: true  
    });
    return false;
});


$('#authenticate-btn').live('click', function(e){
    hide_alert();
    var password = $('#authentication-form').serialize();
    console.log(password);
    $.ajax(
    {
        type: 'POST',
        url: url_base + "/check_password" ,
        data: password,
        success: function(data) 
        { 
            if (data.error != '')
            {
                $('#authentication-modal').modal('hide');
                show_alert(data.error, 'error');
            }
            else
            {
                $('#authentication-modal').modal('hide');
                show_alert('Authentication succesful.', 'success');
                window.setTimeout(function(){location.reload()},2000)
            }
        },
        dataType: "json"
    });
    $('[name=raw_password]').val('');
});

$('#cancel-authenticate-btn').live('click', function(e){
    $('#authentication-modal').modal('hide');
});

var siteID_to_delete = 0;
$.validity.setup({ outputMode:'custom' });

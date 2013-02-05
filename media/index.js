//toggle site form
$(document).ready(function() {
    $(".site_row > td").not('.delete-site-container').click(function(e){
        var target = $(e.target).attr('href');
        if (typeof target == 'undefined' || target == false){
            var $el = $(this).parents('.site_row');
            $el.addClass("hidden");
            var edit_form = $el.attr("id") + "_form";
            $("#"+edit_form).removeClass("hidden");
            return false;
        };
    });
    $(".editsite_cancel_btn").click(function(e){
        var form = $(this).parent().parent().parent().parent()
        form.addClass("hidden");
        var site = "site_" + form.attr("data-site");
        $("#"+site).removeClass("hidden");
        return false;
    });
    $("#addsite_btn").click(function(e){
        $("#addsite_form").removeClass("hidden");
        $("#addsite_btn").addClass("hidden");
        return false;
    });
    $("#addsite_cancel_btn").click(function(e){
        $("#addsite_form").addClass("hidden");
        $("#addsite_btn").removeClass("hidden");
        return false;
    });
    
    $('.delete-site-btn').live('click', function(e) {
        siteID_to_delete = $(this).data('id');
        $('#modal-delete-site').modal({
            backdrop: true,
            show: true	
        });
        return false;
    });
    
    $('#refresh_all_btn').click(function(e) {
        $(this).attr('disabled', 'disabled');
        $(this).text('Testing...');
        refresh_all_sites(this);
    });
    
    $('#addsite_add_btn').click(function(e) {
        add_site();
    });
    
    $('.editsite_save_btn').click(function(e) {
        var theId = $('.editsite_save_btn').data('id');
        var theUrl = $('.editsite_save_btn').data('url')
        edit_site('#site_' + theId, theUrl);
    });
    
    //footer modals
    $('.footer-modal-cancel').click(function(e) {
        cancel_delete();
    });
    $('.footer-modal-delete').click(function(e) {
        delete_site();
    });
    load_tag_cloud();
    
});

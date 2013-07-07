$('document').ready(function() {
    $('.quick-add-unit-submit').click(function(event) {
        event.preventDefault();
        var name = $('.quick-add-unit-name').val();
        var imei = $('.quick-add-unit-imei').val();
        var info_area = $('.quick-add-unit-info');
        var csrf_token = $('.quick-add-unit-form input[csrfmiddlewaretoken]').val();

        if(name == '') {
            info_area.removeClass('alert alert-error alert-success');
            info_area.addClass('alert alert-error');
            info_area.html('Name field cannot be empty');
            return false;
        }

        if(imei == '') {
            info_area.removeClass('alert alert-error alert-success');
            info_area.addClass('alert alert-error');
            info_area.html('IMEI field cannot be empty');
            return false;
        }

        $.post('/api/unit/add.json', 'name='+name+'&imei='+imei)
            .done(function() {
                info_area.removeClass('alert alert-error alert-success');
                info_area.addClass('alert alert-success');
                info_area.html('Unit successfully added');
            })
            .fail(function() {
                info_area.removeClass('alert alert-error alert-success');
                info_area.addClass('alert alert-error');
                info_area.html('XHR query error' + csrf_token);
                return false;
            })
        return true;
    });
});

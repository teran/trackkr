$('document').ready(function() {
    $('.quick-add-unit-submit').click(function(event) {
        event.preventDefault();
        var name = $('.quick-add-unit-name').val();
        var imei = $('.quick-add-unit-imei').val();
        var csrf_token = $('.quick-add-unit-form input[name=csrfmiddlewaretoken]').val();

        if(name == '') {
            $('.notifications')
                .removeClass('alert alert-error alert-success')
                .addClass('alert alert-error')
                .html('Name field cannot be empty');
            return;
        }

        if(imei == '') {
            $('.notifications')
                .removeClass('alert alert-error alert-success')
                .addClass('alert alert-error')
                .html('IMEI field cannot be empty');
            return;
        }

        $.post('/api/unit/add.json', 'name='+name+'&imei='+imei+'&csrfmiddlewaretoken='+csrf_token)
            .done(function() {
                $('.notifications')
                    .removeClass('alert alert-error alert-success')
                    .addClass('alert alert-success')
                    .html('Unit successfully added');
            })
            .fail(function(jqxhr, textStatus, error) {
                $('.notifications')
                    .removeClass('alert alert-error alert-success')
                    .addClass('alert alert-error')
                    .html('jQXHR query error occured');
            });
    });
});

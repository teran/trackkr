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

        $.post('/api/units/add.json', 'name='+name+'&imei='+imei+'&csrfmiddlewaretoken='+csrf_token)
            .done(function() {
                $('.notifications')
                    .removeClass('alert alert-error alert-success')
                    .addClass('alert alert-success')
                    .html('Unit successfully added');
                $.get('/api/units/list.html?limit=5&continue=show')
                    .done(function(data) {
                        $('.units-list').html(data);
                    })
                    .fail(function(jqxhr, textStatus, error) {
                        $('.notifications')
                            .removeClass('alert alert-error alert-success')
                            .addClass('alert alert-error')
                            .html('Error reloading units list');
                    });
            })
            .fail(function(jqxhr, textStatus, error) {
                $('.notifications')
                    .removeClass('alert alert-error alert-success')
                    .addClass('alert alert-error')
                    .html('Error adding unit');
            });
    });
});

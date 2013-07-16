$('document').ready(function() {
    $('.quick-add-unit-submit').click(function(event) {
        event.preventDefault();
        var name = $('.quick-add-unit-name').val();
        var imei = $('.quick-add-unit-imei').val();
        var csrftoken = $.cookie('csrftoken');

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

        var verbose = true
        
        $.post('/api/units/add.json', 'name='+name+'&imei='+imei+'&csrfmiddlewaretoken='+csrftoken)
            .done(function() {
                $('.notifications')
                    .removeClass('alert alert-error alert-success')
                    .addClass('alert alert-success')
                    .html('Unit successfully added');
                $.get('/api/units/list.html?limit=5&continue=show&verbose='+verbose)
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
    $('.unit-delete-button').click(function(event) {
        event.preventDefault();

        var imei = $(this).attr('value');
        var csrftoken = $.cookie('csrftoken');
        
        $('#confirm-delete-modal-'+imei).modal('show');
    });
    $('.unit-delete-button-confirm').click(function(event) {
        event.preventDefault();

        var imei = $(this).attr('value');
        var csrftoken = $.cookie('csrftoken');
        
        $.post('/api/units/delete.json', 'imei='+imei+'&csrfmiddlewaretoken='+csrftoken)
            .done(function() {
                $(location).attr('href', '/units.html');
            })
            .fail(function(jqxhr, textStatus, error) {
                $('.notifications')
                    .removeClass('alert alert-error alert-success')
                    .addClass('alert alert-error')
                    .html('Error deleting unit');
            });
    });
    $('.unit-preferences-save-button').click(function(event) {
        event.preventDefault();

        var imei = $(this).attr('value');
        var csrftoken = $.cookie('csrftoken');

        
        var skip_empty_messages = 0;
        if($('.skip-empty-messages-checkbox').is(':checked')) {
            skip_empty_messages = 1;
        }
        
        var description = $('.unit-description-textarea').val();

        $.post('/api/units/preferences.json?imei='+imei,
               'skip_empty_messages='+skip_empty_messages+'&description='+description+'&csrfmiddlewaretoken='+csrftoken)
            .done(function() {
                $('.notifications')
                    .removeClass('alert alert-error alert-success')
                    .addClass('alert alert-success')
                    .html('Preferences successfully saved');
            })
            .fail(function(jqxhr, textStatus, error) {
                $('.notifications')
                    .removeClass('alert alert-error alert-success')
                    .addClass('alert alert-error')
                    .html('Error saving preferences');
            });
    });
});

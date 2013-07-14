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
    $('.unit-delete-button').click(function() {
        var imei = $(this).attr('value');
        var csrftoken = $.cookie('csrftoken');
        
        $.post('/api/units/delete.json', 'imei='+imei+'&csrfmiddlewaretoken='+csrftoken)
            .done(function() {
                $('.notifications')
                    .removeClass('alert alert-error alert-success')
                    .addClass('alert alert-success')
                    .html('Unit successfully deleted');

                $.get('/api/units/list.html?limit=5&continue=show&verbose=true')
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
                    .html('Error deleting unit');
            });
    });
});

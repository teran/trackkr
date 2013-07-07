$('document').ready(function() {
    $('.quick-add-unit-submit').click(function(event) {
        event.preventDefault();
        var name = $('.quick-add-unit-name').val();
        var imei = $('.quick-add-unit-imei').val();
        var csrf_token = $('.quick-add-unit-form input[csrfmiddlewaretoken]').val();

        if(name == '') {
            $('.notifications').removeClass('alert alert-error alert-success');
            $('.notifications').addClass('alert alert-error');
            $('.notifications').html('Name field cannot be empty');
            return;
        }

        if(imei == '') {
            $('.notifications').removeClass('alert alert-error alert-success');
            $('.notifications').addClass('alert alert-error');
            $('.notifications').html('IMEI field cannot be empty');
            return;
        }

        $.post('/api/unit/add.json', 'name='+name+'&imei='+imei)
            .done(function() {
                $('.notifications').removeClass('alert alert-error alert-success');
                $('.notifications').addClass('alert alert-success');
                $('.notifications').html('Unit successfully added');
            })
            .fail(function(jqxhr, textStatus, error) {
                $('.notifications').removeClass('alert alert-error alert-success');
                $('.notifications').addClass('alert alert-error');
                $('.notifications').html('jQXHR query error occured');
            });
    });

    $('.unit-location-link').click(function(event) {
        event.preventDefault();
        var pk = $(this).attr('href');
        pk = pk.replace('#', '');

        $.getJSON('/api/units/location/'+pk+'.json')
            .done(function(data){
                unit_map.destroy();
                unit_map = new ymaps.Map("unit-map", {
                    center: [data.latitude, data.longitude],
                    zoom: 10
                });

                unit_map.controls
                    .add('zoomControl', { left: 5, top: 5 })
                    .add('typeSelector')
                    .add('mapTools', { left: 35, top: 5 });

                unit_map.geoObjects.add(
                    new ymaps.Placemark(
                        [data.latitude, data.longitude], {
                            balloonContentHeader: data.name,
                            balloonContentBody: data.timestamp
                        }
                    ));
                $('.message-tab-each').removeClass('active');
                $('.message-tab-'+pk).addClass('active');
            })
            .fail(function(jqxhr, textStatus, error) {
                $('.notifications').removeClass('alert alert-error alert-success');
                $('.notifications').addClass('alert alert-error');
                $('.notifications').html('jQXHR query error occured');
            });
    });
});

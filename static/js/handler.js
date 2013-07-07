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
        return true;
    });
});

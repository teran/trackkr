$('document').ready(function(){
    ymaps.ready(function(){
        var imei = $('.unit-imei').text();
        var unit_map;
        $.getJSON('/api/location.json?imei='+imei)
            .done(function(data){
                var recentpos = [data.latitude, data.longitude];
                unit_map = new ymaps.Map("unit-map", {
                        center: recentpos,
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
            })
            .fail(function(jqxhr, textStatus, error) {
                $('.notifications')
                    .removeClass('alert alert-error alert-success')
                    .addClass('alert alert-error')
                    .html('jQXHR query error occured');
            });

        $('.unit-location-link').click(function(event) {
            event.preventDefault();
            var pk = $(this).attr('href');
            var imei = $('.unit-imei').text();
            pk = pk.replace('#', '');
    
            $.getJSON('/api/location.json?imei='+imei+'&message='+pk)
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
                    $('.notifications')
                        .removeClass('alert alert-error alert-success')
                        .addClass('alert alert-error')
                        .html('jQXHR query error occured');
                });
        });
    });
});

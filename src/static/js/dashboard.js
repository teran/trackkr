$('document').ready(function() {
    ymaps.ready(function() {
        var dashboard_map = new ymaps.Map("dashboard-map", {
            center: [ 0, 0 ],
            zoom: 2
            });
        
        dashboard_map.controls
            .add('zoomControl', { left: 5, top: 5 })
            .add('typeSelector')
            .add('mapTools', { left: 35, top: 5 });

        $.getJSON('/api/location.json')
            .done(function(data) {
                $.each(data, function(element, object) {
                    dashboard_map.geoObjects.add(new ymaps.Placemark(
                        [object.latitude, object.longitude], {
                            balloonContentHeader: object.name,
                            balloonContentBody: object.timestamp
                            }
                        ));
                });
            })
            .fail(function(jqxhr, textStatus, error) {
                $('.notifications')
                    .removeClass('alert alert-error alert-success')
                    .addClass('alert alert-error')
                    .html('jQXHR query error occured');
            });
    });
});

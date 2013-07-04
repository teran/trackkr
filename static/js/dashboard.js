$('document').ready(function(){
    ymaps.ready(function(){
        $.getJSON('/api/recentpos.json')
            .done(function(loc){
                var recentpos = [loc.latitude, loc.longitude];
                var dashboard_map = new ymaps.Map("dashboard-map", {
                        center: recentpos,
                        zoom: 10
                    });
                
                dashboard_map.controls
                    .add('zoomControl', { left: 5, top: 5 })
                    .add('typeSelector')
                    .add('mapTools', { left: 35, top: 5 });
    
                $.getJSON('/api/units.json')
                    .done(function(data){
                        $.each(data, function(element, object) {
                            $.getJSON('/api/units/'+object.imei+'.json')
                                .done(function(loc){
                                    dashboard_map.geoObjects.add(new ymaps.Placemark(
                                            [loc.latitude, loc.longitude],
                                            {
                                                balloonContentHeader: loc.name,
                                                balloonContentBody: loc.timestamp
                                            }
                                    ));
                                })
                                .fail(function(jqxhr, textStatus, error){
                                    alert('fail: '+jqxhr+textStatus+error);
                                });
                        });
                })
                .fail(function(jqxhr, textStatus, error){
                    alert('fail: '+jqxhr+textStatus+error);
                });
            })
            .fail(function() {
                alert('Error retrieving latest unit position');
            });
        });
});

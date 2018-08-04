var myMap;
var myPlacemark;

ymaps.ready(init);

function init () {
    myMap = new ymaps.Map('map', {
        center: [55.7408157, 37.608925],
        zoom: 16,
        controls: []
    }, {
        searchControlProvider: 'yandex#search'
    });

}
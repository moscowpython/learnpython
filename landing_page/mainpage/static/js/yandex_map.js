ymaps.ready(function () {
	var myMap = new ymaps.Map('map', {
			center: [55.781774, 37.669752],
			zoom: 17
		}, {
			searchControlProvider: 'yandex#search'
		}),

		// Создаём макет содержимого.

		myPlacemarkWithContent = new ymaps.Placemark([55.781774, 37.669752], {
			hintContent: 'Москва, Русаковская ул., 1',
			balloonContent: '<style>.bal-wrap{width: 260px;}ymaps.ymaps-2-1-69-balloon.ymaps-2-1-69-balloon_layout_normal.ymaps-2-1-69-balloon_to_top.ymaps-2-1-69-i-custom-scroll { top: -209px !important; left: -128px !important; }.ymaps-2-1-69-balloon__tail { left: 44%;}.ymaps-2-1-69-balloon__tail:after {width: 14px; height: 14px;border-bottom: 2px solid #F2C94C; border-left: 2px solid #F2C94C; }ymaps.ymaps-2-1-69-balloon__tail { z-index: 9; box-shadow: none; }.ymaps-2-1-69-balloon__close+.ymaps-2-1-69-balloon__content { margin-right: 0; padding: 0; }.color-yellow{color: #F2C94C;}.color-blue {color: #2D9CDB;}' +
			'@media (max-width: 480px) {' +
			'.bal-wrap{width: 100%;height: 100%;}' +
			'}' +
			'</style> ' +
			'<div class="bal-wrap" style="padding:15px 5px 10px 15px;border: 2px solid #F2C94C; box-sizing: border-box; box-shadow: 0px 5px 10px rgba(0, 0, 0, 0.13);"><span style="font-family: Ubuntu; font-size: 12px">' +
			'<span class="color-blue">L</span>EARN ' +
			'<span class="color-yellow">P</span>YTHON' +
			'</span> ' +
			'<p style="margin:0;font-family: Ubuntu; font-size: 12px">Москва, Русаковская ул., 1 станция метро «Красносельская»</p>' +
			'</div>',

		}, {
			// Опции.
			// Необходимо указать данный тип макета.
			iconLayout: 'default#imageWithContent',
			// Своё изображение иконки метки.
			iconImageHref: 'static/images/icon-svg/pin.svg',
			hideIconOnBalloonOpen: false,
			// Размеры метки.
			iconImageSize: [60, 84],
			// Смещение левого верхнего угла иконки относительно
			// её "ножки" (точки привязки).
			iconImageOffset: [-30, -84],
		});

	myMap.geoObjects

		.add(myPlacemarkWithContent);
});

jQuery(function() {
    // use strict

    luxon.Settings.defaultLocale = 'ru-RU';

    let today = new Date();

    ymaps.ready(function() {
        // Offline map
        (() => {
            let $offline_cities = jQuery('#offline-cities-json'),
                offline_cities = [];

            try {
                offline_cities = JSON.parse($offline_cities.html() || '[]');
            } catch (err) {
                console.error(err);
            }

            if (Array.isArray(offline_cities) === false || offline_cities.length === 0) {
                return;
            }

            let map = new ymaps.Map('offline-map', {
                center: [
                    offline_cities[0].coords[0] - 2,
                    offline_cities[0].coords[1] + 5,
                ],
                zoom: 6
            }, {
                searchControlProvider: 'yandex#search'
            });

            for (let city of offline_cities) {
                let early_date = parse_date(city.early_date),
                    basic_date = parse_date(city.basic_date),
                    placemark = new ymaps.Placemark(city.coords, {
                    balloonContent: `
<div class="offline_city_content_wrapper">
    <h3>${city.name}</h3>
    <div class="offline_city_content_list">
        <div class="offline_city_content_item">
            <p class="title">Ранняя регистрация</p>
            <p class="offline_date">До ${format_date(city.early_date)}</p>
            <p class="offline_price">${format_price(city.early_price)} ₽</p>
            <a href="#howToPay" class="decr-price d-none d-lg-block scroll-to">В рассрочку <strong>от ${format_price(city.early_installment_price)} р/мес</strong></a>
            <button
                ${today > early_date ? 'disabled' : ''}
                data-toggle="modal"
                data-target="#overlay">${today > early_date ? 'Регистрация закрыта' : 'Купить билет'}</button>
        </div>
        <div class="offline_city_content_item">
            <p class="title">Обычная регистрация</p>
            <p class="offline_date">С ${format_date(city.basic_date)}</p>
            <p class="offline_price">${format_price(city.basic_price)} ₽</p>
            <a href="#howToPay" class="decr-price d-none d-lg-block scroll-to">В рассрочку <strong>от ${format_price(city.basic_installment_price)} р/мес</strong></a>
            <button
                ${today < basic_date ? 'disabled' : ''}
                data-toggle="modal"
                data-target="#overlay">${today < basic_date ? `С ${format_date_with_year(basic_date)}` : 'Купить билет'}</button>
        </div>
    </div>
</div>`
                }, {
                    // Опции.
                    // Необходимо указать данный тип макета.
                    iconLayout: 'default#imageWithContent',
                    // Своё изображение иконки метки.
                    iconImageHref: 'static/images/yellow-mark.svg',
                    hideIconOnBalloonOpen: false,
                    // Размеры метки.
                    iconImageSize: [28, 40],
                    // Смещение левого верхнего угла иконки относительно
                    // её "ножки" (точки привязки).
                    iconImageOffset: [-14, -40],

                    balloonOffset: [30, 340],
                    balloonMaxWidth: 570,
                    balloonMinWidth: 570,
                    balloonMaxHeight: 317,
                    balloonMinHeight: 317,
                    balloonCloseButton: false,
                    balloonAutoPanMargin: 150
                });

                city.placemark = placemark;

                placemark.events.add('balloonopen', function() {
                    activateCityByName(city.name);

                    placemark.options.set('iconImageHref', 'static/images/blue-mark.svg');
                    placemark.options.set('iconImageSize', [42, 60]);
                    placemark.options.set('iconImageOffset', [-21, -60]);
                });

                placemark.events.add('balloonclose', function() {
                    placemark.options.set('iconImageHref', 'static/images/yellow-mark.svg');
                    placemark.options.set('iconImageSize', [28, 40]);
                    placemark.options.set('iconImageOffset', [-14, -40]);
                });

                map.geoObjects.add(placemark);
            }

            activateCityByName(offline_cities[0].name);

            jQuery(document).on('click', '[data-offline-city-name]', function(e) {
                e.preventDefault();

                let $this = jQuery(this);

                activateCityByName($this.data('offline-city-name'));
            });

            function activateCityByName(city_name) {
                jQuery('[data-offline-city-name]').removeClass('active');
                jQuery(`[data-offline-city-name="${city_name}"]`).addClass('active');

                let city = offline_cities.find(({name}) => name === city_name);

                city?.placemark?.balloon.open();
            }
        })();

        // Footer map
        (() => {
            let map = new ymaps.Map('map', {
                center: [55.755988, 37.643448],
                zoom: 16
            }, {
                searchControlProvider: 'yandex#search'
            });

            map.geoObjects.add(new ymaps.Placemark([55.755988, 37.643448], {
                hintContent: 'Хохловский пер., 7-9с2, подъезд 3, этаж 1',
                balloonContent: '<style>.bal-wrap{width: 260px;}ymaps.ymaps-2-1-69-balloon.ymaps-2-1-69-balloon_layout_normal.ymaps-2-1-69-balloon_to_top.ymaps-2-1-69-i-custom-scroll { top: -209px !important; left: -128px !important; }.ymaps-2-1-69-balloon__tail { left: 44%;}.ymaps-2-1-69-balloon__tail:after {width: 14px; height: 14px;border-bottom: 2px solid #F2C94C; border-left: 2px solid #F2C94C; }ymaps.ymaps-2-1-69-balloon__tail { z-index: 9; box-shadow: none; }.ymaps-2-1-69-balloon__close+.ymaps-2-1-69-balloon__content { margin-right: 0; padding: 0; }.color-yellow{color: #F2C94C;}.color-blue {color: #2D9CDB;}' +
                    '@media (max-width: 480px) {' +
                    '.bal-wrap{width: 100%;height: 100%;}' +
                    '}' +
                    '</style> ' +
                    '<div class="bal-wrap" style="padding:15px 5px 10px 15px;border: 2px solid #F2C94C; box-sizing: border-box; box-shadow: 0px 5px 10px rgba(0, 0, 0, 0.13);"><span style="font-family: Ubuntu; font-size: 12px">' +
                    '<span class="color-blue">L</span>EARN ' +
                    '<span class="color-yellow">P</span>YTHON' +
                    '</span> ' +
                    '<p style="margin:0;font-family: Ubuntu; font-size: 12px">Хохловский пер., 7-9с2, подъезд 3, этаж 1, станция метро «Китай-город»</p>' +
                    '</div>'

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
                iconImageOffset: [-30, -84]
            }));
        })();
    });

    function format_price(price) {
        return new Intl.NumberFormat('ru-RU').format(price);
    }

    function parse_date(date) {
        return luxon.DateTime.fromISO(date);
    }

    function format_date(date) {
        return parse_date(date).toLocaleString({month: "long", day: "numeric"});
    }

    function format_date_with_year(date) {
        return parse_date(date).toLocaleString(luxon.DateTime.DATE_FULL);
    }
});

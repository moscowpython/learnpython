jQuery(function() {
    'use strict';
    let $body = jQuery('body');

    // MOBILE CAROUSEL PROJECT LIST START
    (() => {
        let $carousel = jQuery('.projects_list'),
            $slick = null;

        if ($carousel.length === 0) {
            return;
        }

        function slickToggle() {
            if (window.innerWidth > 750 && $slick) {
                $slick.slick('unslick');
                $slick = null;
            } else if (window.innerWidth <= 750 && !$slick) {
                $slick = $carousel.slick({
                    dots: true,
                    infinite: true,
                    speed: 300,
                    slidesToShow: 1,
                    arrows: false,
                    variableWidth: true
                });
            }
        }

        jQuery(window).on('resize', function(e) {
            slickToggle();
        });

        slickToggle();
    })();
    // MOBILE CAROUSEL PROJECT LIST END

    // SECTION POSTS CAROUSEL START
    jQuery('.posts_carousel').slick({
        infinite: true,
        slidesToShow: 2,
        slidesToScroll: 1,
        responsive: [
            {
                breakpoint: 750,
                settings: {
                    slidesToShow: 1,
                    slidesToScroll: 1,
                    infinite: true
                }
            }
        ],
        prevArrow: '<button type="button" class="slick-prev slick-arrow"><i class="fa fa-arrow-left" aria-hidden="true"> <span>Предыдущие посты</span></i></button>',
        nextArrow: '<button type="button" class="slick-next slick-arrow"><span>Следующий пост</span> <i class="fa fa-arrow-right" aria-hidden="true"></i></button>'
    });
    // SECTION POSTS CAROUSEL END

    // SECTION POST PREVIEW CAROUSEL START
    jQuery('.post_preview_carousel').slick({
        infinite: true,
        slidesToShow: 1,
        slidesToScroll: 1,
        prevArrow: false,
        nextArrow: '<button type="button" class="slick-next slick-arrow"><span>Следующая статья </span> <i class="fa fa-arrow-right" aria-hidden="true"></i></button>'
    });
    // SECTION POST PREVIEW CAROUSEL END

    // MOBILE MENU START
    jQuery('.mobile_menu_btn').on('click', function(e) {
        e.preventDefault();
        $body.toggleClass('mobile-menu-opened');
    });

    jQuery('.mobile_menu_bg').on('click', function() {
        $body.removeClass('mobile-menu-opened');
    });
    // MOBILE MENU END

    // SECTION SEARCH SELECT BLOCK START
    jQuery('.select_wrapper select').each(function() {
        let $this = jQuery(this);

        $this.select2({
            minimumResultsForSearch: Infinity,
            placeholder: 'Поиск по городам',
            dropdownParent: $this.closest('.select_wrapper'),
            width: '100%'
        });
    });
    // SECTION SEARCH SELECT BLOCK END

    setTimeout(() => {
        $body.removeClass('loading');
    }, 1000);
});

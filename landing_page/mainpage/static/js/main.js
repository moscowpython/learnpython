'use strict';

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

var LearnPython = function () {
  function LearnPython() {
    _classCallCheck(this, LearnPython);

    this.$navbar = $('.nav-bar');
    this.$header = $('.main-header');
    this.reviewsSlider = null;
    this.teacherSlider = null;
    this.calendarSlider = null;
    this.init();
  }

  _createClass(LearnPython, [{
    key: 'init',
    value: function init() {
      //this.typedText();
      this.fixHeader();
      this.initSlider();
      this.initTabNav();
      this.navbarToggle();
      this.startCounter();
      this.initScrollTo();
      this.scrollWatcher();
      this.animateOnReady();
      this.customTabsInit();
      this.modalTypeSelector();
      this.initSliderReviews();
      this.initHistorySliders();
      this.sectionCollapseInit();
    }
  }, {
    key: 'fixHeader',
    value: function fixHeader() {
      this.$header[($(window).scrollTop() > 20 ? 'add' : 'remove') + 'Class']('scrolled');
    }
  }, {
    key: 'animateOnReady',
    value: function animateOnReady() {
      $(function () {
        $('.animated-on-ready').addClass('animated');
      });
    }
  }, {
    key: 'typedText',
    value: function typedText() {
      // js-type-it
      var word = $('.js-type-it');
      var cortege = word.text().split('');
      cortege = cortege.map(function (item) {
        return '<span>' + item + '</span>';
      });
      word.html(cortege);

      runForward(word);

      function runForward($word) {
        var items = $word.find('span');
        var index = 0;
        var intervalForward = window.setInterval(function () {
          if (!items.length) return;
          $word.children().eq(index).addClass('color-yellow');
          index++;
          if (index >= items.length) {
            window.clearInterval(intervalForward);
            window.setTimeout(function () {
              runBack($word);
            }, 1000);
          }
        }, 300);
      }

      function runBack($word) {
        var items = $word.find('span');
        var index = items.length;
        var intervalBack = window.setInterval(function () {
          if (!items.length) return;
          $word.children().eq(index).removeClass('color-yellow');
          index--;
          if (index < 0) {
            window.clearInterval(intervalBack);
            window.setTimeout(function () {
              runForward($word);
            }, 1000);
          }
        }, 200);
      }
    }
  }, {
    key: 'scrollWatcher',
    value: function scrollWatcher() {
      var _this = this;

      $(window).on('scroll', function () {
        _this.fixHeader();
      });
    }
  }, {
    key: 'initSlider',
    value: function initSlider() {
      $('.examples-slider').slick({
        centerMode: true,
        dots: true,
        initialSlide: 1,
        infinite: false,
        slidesToShow: 3,
        adaptiveHeight: false,
        arrows: true,
        centerPadding: '0'
      });
    }
  }, {
    key: 'initSliderReviews',
    value: function initSliderReviews() {
      this.reviewsSlider = $('.reviews-carousel-slider').slick({
        nextArrow: '.carousel-control.next',
        prevArrow: '.carousel-control.prev',
        dots: true,
        adaptiveHeight: true,
        appendDots: $('.pagerSelector'),
        customPaging: function customPaging(slider, pageIndex) {
          return ++pageIndex + '/' + slider.slideCount;
        }

      });
    }
  }, {
    key: 'initTabNav',
    value: function initTabNav() {
      $('.tab-nav-container a').on('click', function () {
        var $this = $(this);
        var $parent = $this.closest('.tab-nav-container');
        var target = $parent.data('target');
        var container = $parent.siblings('[data-nav="' + target + '"]');
        var currIndex = container.find('.show').index();

        $this.hasClass('next') ? currIndex++ : currIndex--;
        if (currIndex > 2 || currIndex < 0) return;

        container.children().eq(currIndex).siblings().removeClass('show').end().addClass('show');
      });
    }
  }, {
    key: 'initScrollTo',
    value: function initScrollTo() {
      var _this2 = this;

      $('a.scroll-to').on('click', function (e) {
        e.preventDefault();
        var link = $(e.target).closest('a');
        _this2.toggleCollapsing($(link.attr('href')));
        _this2._smoothScroll(link.attr('href'));
        _this2._isSmallScreen() && _this2.$navbar.removeClass('open');
        _this2._afterToggleCallback($(link.attr('href')));
      });
      $('button.scroll-to').on('click', function (e) {
        var link = $(e.target).closest('button');
        _this2._smoothScroll(link.data('target'));
        _this2.toggleCollapsing($(link.data('target')));
        _this2._afterToggleCallback($(link.data('target')));
      });
    }
  }, {
    key: '_smoothScroll',
    value: function _smoothScroll(selector) {
      var target = $(selector).offset().top;
      var body = $("html, body");
      body.stop().animate({
        scrollTop: target
      }, 500, 'swing');
    }
  }, {
    key: 'startCounter',
    value: function startCounter() {
      var container = $('.counter-container');
      var modalTime = $('.time-target');
      var countDownDate = new Date(container.data('countDown')).getTime();
      var x = setInterval(function () {
        var distance = countDownDate - new Date().getTime();
        var date = {
          days: Math.floor(distance / (1000 * 60 * 60 * 24)),
          hours: Math.floor(distance % (1000 * 60 * 60 * 24) / (1000 * 60 * 60)),
          minutes: Math.floor(distance % (1000 * 60 * 60) / (1000 * 60)),
          seconds: Math.floor(distance % (1000 * 60) / 1000)
        };
        container.html('\n<div><b class="d-block">' + date.days + '</b><span>\u0434\u043D\u0435\u0439</span></div><span class="delimeter">:</span>\n<div><b class="d-block">' + date.hours + '</b><span>\u0447\u0430\u0441\u043E\u0432</span></div><span class="delimeter">:</span>\n<div><b class="d-block">' + date.minutes + '</b><span>\u043C\u0438\u043D\u0443\u0442</span></div><span class="delimeter">:</span>\n<div><b class="d-block">' + date.seconds + '</b><span>\u0441\u0435\u043A\u0443\u043D\u0434</span></div>\n        ');
        modalTime.text('\u0417\u0430\u043A\u0440\u044B\u0442\u0438\u0435 \u0440\u0435\u0433\u0438\u0441\u0442\u0440\u0430\u0446\u0438\u0438 \u0447\u0435\u0440\u0435\u0437 ' + date.days + ' \u0434\u043D\u0435\u0439 ' + date.hours + ' \u0447\u0430\u0441\u043E\u0432');
        if (distance < 0) {
          clearInterval(x);
          modalTime.text('Регистрация завершена');
          container.html('Регистрация завершена');
        }
      }, 1000);
    }
  }, {
    key: 'modalTypeSelector',
    value: function modalTypeSelector() {
      $('.type-selector').on('click', function (event) {
        var $this = $(event.target).closest('.type-selector');
        var cost = $this.find('.cost').text();
        $('.total-selected').text(cost);
      });
    }
  }, {
    key: 'navbarToggle',
    value: function navbarToggle() {
      var _this3 = this;

      $('.navbar-toggle').on('click', function () {
        return _this3.$navbar.toggleClass('open');
      });
    }
  }, {
    key: '_isSmallScreen',
    value: function _isSmallScreen() {
      return window.innerWidth < 992;
    }
  }, {
    key: 'sectionCollapseInit',
    value: function sectionCollapseInit() {
      var _this4 = this;

      $('.m-section-header').on('click', function (e) {
        var target = $(e.target).closest('.m-section-header');
        var section = target.closest('section');
        _this4.toggleCollapsing(section);
        _this4._afterToggleCallback(section);
        _this4._smoothScroll('#' + section.attr('id'));
      });
    }
  }, {
    key: 'toggleCollapsing',
    value: function toggleCollapsing(section) {
      section.toggleClass('show').siblings('section').removeClass('show');
    }
  }, {
    key: '_initCalendarSlider',
    value: function _initCalendarSlider() {
      this.calendarSlider = $('.calendar-list').slick({
        infinite: false,
        arrows: false,
        dots: true
      });
    }
  }, {
    key: '_destroyCalendarSlider',
    value: function _destroyCalendarSlider() {
      if (this.calendarSlider) {
        this.calendarSlider.slick('unslick');
      }
    }
  }, {
    key: '_initTeacherSlider',
    value: function _initTeacherSlider() {
      this.teacherSlider = $('.mentor-list').slick({
        infinite: false,
        arrows: false,
        dots: true
      });
    }
  }, {
    key: '_destroyTeacherSlider',
    value: function _destroyTeacherSlider() {
      if (this.teacherSlider) {
        this.teacherSlider.slick('unslick');
      }
    }
  }, {
    key: 'reactivateReviewsCarousel',
    value: function reactivateReviewsCarousel() {
      this.reviewsSlider.slick('unslick');
      this.initSliderReviews();
    }
  }, {
    key: 'customTabsInit',
    value: function customTabsInit() {
      $('.custom-tab').on('click', function (e) {
        var target = $(e.target).closest('.custom-tab');
        var selector = target.data('target');
        target.addClass('active').siblings().removeClass('active');
        $('.tab-holder').removeClass('bg-yellow bg-blue').addClass(selector === '.online-tab' ? 'bg-yellow' : 'bg-blue');
        $('.online-tab, .offline-tab').removeClass('active');
        $(selector).addClass('active');
      });
    }
  }, {
    key: '_afterToggleCallback',
    value: function _afterToggleCallback(section) {
      if (this._isSmallScreen()) {
        if (section.hasClass('calendar') && section.hasClass('show')) {
          this._initCalendarSlider();
        } else if (section.hasClass('teachers') && section.hasClass('show')) {
          this._initTeacherSlider();
        } else if (section.hasClass('reviews') && section.hasClass('show')) {
          this.reactivateReviewsCarousel();
        } else {
          this._destroyCalendarSlider();
          this._destroyTeacherSlider();
        }
      }
    }
  }, {
    key: 'initHistorySliders',
    value: function initHistorySliders() {
      //   $('.history-slider').each(function () {
      //     const $this = $(this);
      //     const target = $this.data('nav');
      //
      //     $this.slick({
      //       infinite: false,
      //       nextArrow: `.${target} .next`,
      //       prevArrow: `.${target} .prev`,
      //     })
      //   })
      //
      //
    }
  }]);

  return LearnPython;
}();

var learnPython = new LearnPython();
//# sourceMappingURL=main.js.map
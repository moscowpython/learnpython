class LearnPython {

  constructor() {
    this.$navbar = $('.nav-bar');
    this.$header = $('.main-header');
    this.reviewsSlider = null;
    this.teacherSlider = null;
    this.calendarSlider = null;
    this.init();
  }

  init() {
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

  fixHeader() {
    this.$header[`${$(window).scrollTop() > 20 ? 'add' : 'remove'}Class`]('scrolled');
  }

  animateOnReady() {
    $(() => {
      $('.animated-on-ready').addClass('animated')
    });
  }

  typedText() {
    // js-type-it
    const word = $('.js-type-it');
    let cortege = word.text().split('');
    cortege = cortege.map(item => `<span>${item}</span>`);
    word.html(cortege);

    runForward(word);

    function runForward($word) {
      let items = $word.find('span');
      let index = 0;
      let intervalForward = window.setInterval(function () {
        if (!items.length) return;
        $word.children().eq(index).addClass('color-yellow');
        index++;
        if(index >= items.length){
          window.clearInterval(intervalForward);
          window.setTimeout(function () {
            runBack($word);
          }, 1000)
        }
      }, 300)
    }
    
    function runBack($word) {
      let items = $word.find('span');
      let index = items.length;
      let intervalBack = window.setInterval(function () {
        if (!items.length) return;
        $word.children().eq(index).removeClass('color-yellow');
        index--;
        if(index < 0){
          window.clearInterval(intervalBack);
          window.setTimeout(function () {
            runForward($word);
          }, 1000)
        }
      }, 200)
    }
  }

  scrollWatcher() {
    $(window).on('scroll', () => {
      this.fixHeader();
    })
  }

  initSlider() {
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

  initSliderReviews() {
    this.reviewsSlider = $('.reviews-carousel-slider').slick({
      nextArrow: '.carousel-control.next',
      prevArrow: '.carousel-control.prev',
      dots: true,
      adaptiveHeight: true,
      appendDots: $('.pagerSelector'),
      customPaging: function (slider, pageIndex) {
        return ++pageIndex + '/' + slider.slideCount;
      }

    })
  }

  initTabNav() {
    $('.tab-nav-container a').on('click', function () {
      const $this = $(this);
      const $parent = $this.closest('.tab-nav-container');
      const target = $parent.data('target');
      const container = $parent.siblings(`[data-nav="${target}"]`);
      let currIndex = container.find('.show').index();

      $this.hasClass('next') ? currIndex++ : currIndex--;
      if (currIndex > 2 || currIndex < 0) return;

      container.children().eq(currIndex)
        .siblings().removeClass('show')
        .end().addClass('show')
    });
  }

  initScrollTo() {
    $('a.scroll-to').on('click', e => {
      e.preventDefault();
      const link = $(e.target).closest('a');
      this.toggleCollapsing($(link.attr('href')));
      this._smoothScroll(link.attr('href'));
      this._isSmallScreen() && this.$navbar.removeClass('open');
      this._afterToggleCallback($(link.attr('href')));
    });
    $('button.scroll-to').on('click', e => {
      const link = $(e.target).closest('button');
      this._smoothScroll(link.data('target'));
      this.toggleCollapsing($(link.data('target')));
      this._afterToggleCallback($(link.data('target')));
    });
  }

  _smoothScroll(selector) {
    const target = $(selector).offset().top;
    const body = $("html, body");
    body.stop().animate({
      scrollTop: target
    }, 500, 'swing')
  }

  startCounter() {
    const container = $('.counter-container');
    const modalTime = $('.time-target');
    const countDownDate = new Date(container.data('countDown')).getTime();
    const x = setInterval(function () {
      const distance = countDownDate - new Date().getTime();
      const date = {
        days: Math.floor(distance / (1000 * 60 * 60 * 24)),
        hours: Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)),
        minutes: Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60)),
        seconds: Math.floor((distance % (1000 * 60)) / 1000)
      };
      container.html(`
<div><b class="d-block">${date.days}</b><span>дней</span></div><span class="delimeter">:</span>
<div><b class="d-block">${date.hours}</b><span>часов</span></div><span class="delimeter">:</span>
<div><b class="d-block">${date.minutes}</b><span>минут</span></div><span class="delimeter">:</span>
<div><b class="d-block">${date.seconds}</b><span>секунд</span></div>
        `);
      modalTime.text(`Закрытие регистрации через ${date.days} дней ${date.hours} часов`);
      if (distance < 0) {
        clearInterval(x);
        modalTime.text('Регистрация завершена');
        container.html('Регистрация завершена');
      }
    }, 1000);
  }

  modalTypeSelector() {
    $('.type-selector').on('click', event => {
      const $this = $(event.target).closest('.type-selector');
      const cost = $this.find('.cost').text();
      $('.total-selected').text(cost);
    });
  }

  navbarToggle() {
    $('.navbar-toggle').on('click', () => this.$navbar.toggleClass('open'))
  }

  _isSmallScreen() {
    return window.innerWidth < 992
  }

  sectionCollapseInit() {
    $('.m-section-header').on('click', e => {
      const target = $(e.target).closest('.m-section-header');
      const section = target.closest('section');
      this.toggleCollapsing(section);
      this._afterToggleCallback(section);
      this._smoothScroll('#' + section.attr('id'));
    });
  }

  toggleCollapsing(section) {
    section.toggleClass('show')
      .siblings('section')
      .removeClass('show');
  }

  _initCalendarSlider() {
    this.calendarSlider = $('.calendar-list').slick({
      infinite: false,
      arrows: false,
      dots: true,
    })
  }

  _destroyCalendarSlider() {
    if (this.calendarSlider) {
      this.calendarSlider.slick('unslick');
    }
  }

  _initTeacherSlider() {
    this.teacherSlider = $('.mentor-list').slick({
      infinite: false,
      arrows: false,
      dots: true,
    })
  }

  _destroyTeacherSlider() {
    if (this.teacherSlider) {
      this.teacherSlider.slick('unslick');
    }
  }

  reactivateReviewsCarousel() {
    this.reviewsSlider.slick('unslick');
    this.initSliderReviews();
  }

  customTabsInit() {
    $('.custom-tab').on('click', e => {
      const target = $(e.target).closest('.custom-tab');
      const selector = target.data('target');
      target.addClass('active').siblings().removeClass('active');
      $('.tab-holder').removeClass('bg-yellow bg-blue')
        .addClass(selector === '.online-tab' ? 'bg-yellow' : 'bg-blue');
      $('.online-tab, .offline-tab').removeClass('active');
      $(selector).addClass('active');
    })
  }

  _afterToggleCallback(section) {
    if (this._isSmallScreen()) {
      if (section.hasClass('calendar') && section.hasClass('show')) {
        this._initCalendarSlider();
      } else if (section.hasClass('teachers') && section.hasClass('show')) {
        this._initTeacherSlider();
      } else if (section.hasClass('reviews') && section.hasClass('show')) {
        this.reactivateReviewsCarousel()
      } else {
        this._destroyCalendarSlider();
        this._destroyTeacherSlider();
      }
    }
  }

  initHistorySliders() {
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
}

const learnPython = new LearnPython();

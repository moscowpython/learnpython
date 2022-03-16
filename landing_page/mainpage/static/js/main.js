class LearnPython {

	constructor() {
		this.$navbar = $('.nav-bar');
		this.$header = $('.main-header');
		this.reviewsSlider = null;
		this.teacherSlider = null;
		this.aboutSlider = null;
		this.timetableSlider = null;
		this.mobiOpeWeek = null;
		this.init();
	}

	init() {
		this.initScrollupbut();
		this.fixHeader();
		this.initSlider();
		// this.initSimpleBar();
		this.initOnlineSlider();
		this.mobiTimetableInit();
		this.initTeacherSlider();
		this.initTabNav();
		this.navbarToggle();
		this.startCounter();
		this.initScrollTo();
		this.scrollWatcher();
		this.animateOnReady();
		this.customTabsInit();
		this.modalTypeSelector();
		this.initSliderReviews();
		this.sectionCollapseInit();
		this.initAboutSlider();
	}

	fixHeader() {
		this.$header[`${$(window).scrollTop() > 20 ? 'add' : 'remove'}Class`]('scrolled');
	}

	initScrollupbut() {
		$(function (f) {
			var element = f('#scrollup');
			f(window).scroll(function () {
				(f(this).scrollTop() > 3368) ? element.show(300): element.hide(300);
				if(f(this).scrollTop() > 3368) {
					($('#scrollup').offset().top > $('#contact').offset().top ) ? element.fadeTo(0,1): element.fadeTo(0,0.5);
				}
			});
		});
		$('#scrollup').on('click', function () {
			$('body,html').animate({
				scrollTop: 0
			}, 800);
			return false;
		});
	}

	animateOnReady() {
		$(() => {
			$('.animated-on-ready').addClass('animated')
		});
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
			infinite: true,
			adaptiveHeight: false,
			slidesToShow: 3,
			prevArrow: '<button class="slick-prev" type="button"></button>',
			nextArrow: '<button class="slick-next" type="button"></button>',
			arrows: true,
			centerPadding: '0'
		});
	}

	initSimpleBar() {
		if (window.matchMedia('(min-width: 1160px)').matches){
			new SimpleBar(document.getElementById('city-simplebar'));
		}

		if (window.matchMedia('(min-width: 1160px)').matches){
			new SimpleBar(document.getElementById('upper-city-simplebar'));
		}
	}

	initOnlineSlider() {
		if (!this.timetableSlider) {
			this.timetableSlider = $('.online-timetable, .offline-timetable').slick({
				centerMode: false,
				dots: false,
				initialSlide: 0,
				infinite: false,
				slidesToShow: 1,
				prevArrow: '<button class="time-tb-button slick-prev" type="button"><i class="material-icons"> arrow_back </i></button>',
				nextArrow: '<button class="time-tb-button slick-next" type="button"><i class="material-icons"> arrow_forward </i></button>',
				arrows: true,
				adaptiveHeight: true,
				centerPadding: '0'
			});
		}
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
		});
		$('button.scroll-to').on('click', e => {
			const link = $(e.target).closest('button');
			this._smoothScroll(link.data('target'));
			this.toggleCollapsing($(link.data('target')));
		});
	}

	_smoothScroll(selector) {
		let target;
		(this._isSmallScreen()) ? target = $(selector).offset().top -50 : target = $(selector).offset().top;
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
			date.days < 10 ? date.days = "0" + date.days : date.days = "" + date.days;
			date.hours < 10 ? date.hours = "0" + date.hours : date.hours = "" + date.hours;
			date.minutes < 10 ? date.minutes = "0" + date.minutes : date.minutes = "" + date.minutes;
			date.seconds < 10 ? date.seconds = "0" + date.seconds : date.seconds = "" + date.seconds;
			container.html(`
<div class="row justify-content-center"><b class="d-block">${date.days}</b><span class="tm-name">дней</span></div><span class="delimeter">:</span>
<div class="row justify-content-center"><b class="d-block">${date.hours}</b><span class="tm-name">часов</span></div><span class="delimeter">:</span>
<div class="row justify-content-center"><b class="d-block">${date.minutes}</b><span class="tm-name">минут</span></div><span class="delimeter">:</span>
<div class="row justify-content-center"><b class="d-block">${date.seconds}</b><span class="tm-name">секунд</span></div>
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
		$('.navbar-toggle').on('click', () => {
			this.$navbar.toggleClass('open')
		})
	}

	_isSmallScreen() {
		return window.innerWidth < 992
	}

	sectionCollapseInit() {
		$('.m-section-header').on('click', e => {
			const target = $(e.target).closest('.m-section-header');
			const section = target.closest('section');
			this.toggleCollapsing(section);
			this._smoothScroll('#' + section.attr('id'));
		});

		if (this._isSmallScreen()) {
			this._destroyTimetableSlider();
		}
		$(window).on('resize', e => {
			if (this._isSmallScreen()) {
				this._destroyTimetableSlider();
				this.mobiTimetableInit();
				this.initTeacherSlider();
				this.initAboutSlider();
			} else {
				this._destroyWeekEvent();
				this.initOnlineSlider();
				this._destroyTeacherSlider();
				this._destroyAboutSlider();

			}

		});
	}

	toggleCollapsing(section) {

		section.toggleClass('show')
			.siblings('section')
			.removeClass('show');

	}

	initTeacherSlider() {
		if (!this.teacherSlider && this._isSmallScreen()) {
			this.teacherSlider = $('.mentor-list').slick({
				infinite: false,
				arrows: false,
				dots: true,
				adaptiveHeight: true,

			})
		}
	}

	initAboutSlider() {
		if (!this.aboutSlider && this._isSmallScreen()) {
			// this.aboutSlider = $('.about-grid-block').slick({
			// 	infinite: true,
			// 	arrows: false,
			// 	dots: true,
			// 	initialSlide: 3,
			// 	adaptiveHeight: true,
			// })
		}
	}

	_destroyTeacherSlider() {
		if (this.teacherSlider) {
			this.teacherSlider.slick('unslick');
			this.teacherSlider = null;
		}
	}

	_destroyAboutSlider() {
		if (this.aboutSlider) {
			this.aboutSlider.slick('unslick');
			this.aboutSlider = null;
		}
	}

	_destroyTimetableSlider() {
		if (this.timetableSlider) {
			this.timetableSlider.slick('unslick');
			this.timetableSlider = null;
		}
	}

	// _addEventsWeek(e) {
	// 	console.log(currentTarget)
	// 	const currentTarget = $(e.currentTarget).children('i');
	// 	const nextTarget = $(e.currentTarget).next('.week-content');
	// 	nextTarget.toggleClass('show-week');
	// 	$('.week-title-onl > i, .week-title-offln > i').each(function (i,el) {
	// 		if (currentTarget[0] != el) {
	// 			$( this )[0].innerText = 'keyboard_arrow_down';
	// 		}
	// 	});
	// 	$('.week-content.show-week').each(function (i,el){
	// 		if (nextTarget[0] != el) {
	// 			$( this ).removeClass('show-week');
	// 		}
	// 	});
	// 	(currentTarget[0].innerText == "keyboard_arrow_up") ? currentTarget[0].innerText = "keyboard_arrow_down" :
	// 		currentTarget[0].innerText = "keyboard_arrow_up";
	// }

	mobiTimetableInit() {
		if (this._isSmallScreen() && (!this.mobiOpeWeek)) {
			this.mobiOpeWeek = $('.timetable-container .tab-content').slick({
				infinite: true,
				prevArrow: '<button class="time-tb-button slick-prev" type="button"><i class="material-icons"> arrow_back </i></button>',
				nextArrow: '<button class="time-tb-button slick-next" type="button"><i class="material-icons"> arrow_forward </i></button>',
				arrows: true,
				dots: true,
				adaptiveHeight: true,
				fade: true

			})
			// this.mobiOpeWeek = $('div.timetable-title-onl, div.timetable-title-offln').on('click', this._addEventsWeek);
		}
	}

	_destroyWeekEvent() {
		if (!this._isSmallScreen() && (this.mobiOpeWeek)) {
			this.mobiOpeWeek.slick('unslick');
			this.mobiOpeWeek = null;
		}
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

}

const learnPython = new LearnPython();

from django.db import models


class MoscowPythonMeetup(models.Model):

	class Meta:
		verbose_name_plural = "MoscowPython Митапы"

	def __str__(self):
		return f'MoscowPython Meetup № {self.meetup_number}'

	meetup_number = models.IntegerField(
		verbose_name='Номер митапа'
	)

	meetup_day = models.IntegerField(
		verbose_name='День Митапа'
	)

	months_list = [
		('Января', 'Январь'),
		('Февраля', 'Февраль'),
		('Марта', 'Март'),
		('Апреля', 'Апрель'),
		('Мая', 'Май'),
		('Июня', 'Июнь'),
		('Июля', 'Июль'),
		('Августа', 'Август'),
		('Сентября', 'Сентябрь'),
		('Октября', 'Октябрь'),
		('Ноября', 'Ноябрь'),
		('Декабря', 'Декабрь')
	]

	meetup_month = models.TextField(
		choices=months_list,
		default='Январь',
		verbose_name='Месяц Митапа'
	)

	meetup_time = models.TimeField(
		blank=True,
		auto_now=True,
		verbose_name='Время Митапа'
	)

	meetup_link = models.URLField(
		default='http://www.moscowpython.ru'
	)


class LearnPythonCourse(models.Model):
	class Meta:
		verbose_name_plural = "LearnPython Наборы"

	def __str__(self):
		return f'LearnPython Набор № {self.course_index}'

	course_index = models.IntegerField(
		verbose_name='Набор №'
	)

	course_start_date = models.DateField(
		verbose_name='Дата начала курса'
	)

	course_end_date = models.DateField(
		verbose_name='Дата окончания курса'
	)

	online_gepard_price = models.IntegerField(
		verbose_name='Цена "Гепард" (Онлайн)'
	)

	online_gepard_due_date = models.DateField(
		verbose_name='"Гепард" (Онлайн) действительна до'
	)

	online_mustang_price = models.IntegerField(
		verbose_name='Цена "Мустанг" (Онлайн)'
	)

	online_mustang_due_date = models.DateField(
		verbose_name='"Мустанг" (Онлайн) действительна до'
	)

	online_panda_price = models.IntegerField(
		verbose_name='Цена "Панда" (Онлайн)'
	)

	online_panda_due_date = models.DateField(
		verbose_name='"Панда" (Онлайн) действительна до'
	)


class Courators(models.Model):
	class Meta:
		verbose_name_plural = "LearnPython Кураторы"

	def __str__(self):
		return f'Куратор {curator_name}'

	curator_name = models.CharField(
		max_length=50,
		verbose_name='Имя и фамилия куратора'
	)

	curator_bio = models.TextField(
		verbose_name='Биография куратора'
	)

	curator_motto = models.CharField(
		max_length=150,
		verbose_name='Девиз куратора'
	)

	curator_photo = models.ImageField(

	)

	courator_status = models.BooleanField(
		verbose_name="Куратор для ближайшего набора?",
		default=True
	)

	courator_github = models.URLField(
		blank=True,
	)

	courator_social_network = models.URLField(
		blank=True
	)


class Feedback(models.Model):
	class Meta:
		verbose_name_plural = "LearnPython Отзывы"

	def __str__(self):
		return f'Отзыв участника {feedback_author}'

	feedback_author = models.CharField(
		verbose_name='Автор отзыва',
		max_length=50,
		null=True
	)

	feedback_author_link = models.URLField(
		verbose_name='Ссылка на автора',
		blank=True,
		null=True
	)

	feedback_author_position = models.CharField(
		verbose_name='Должность выпускника',
		max_length=50,
		null=True
	)

	feedback_author_photo = models.ImageField(
		null=True
	)

	feedback_text = models.TextField(
		verbose_name='Текст отзыва',
		null=True
	)


class GraduateProjects(models.Model):
	class Meta:
		verbose_name_plural = "LearnPython Проекты учеников"

	def __str__(self):
		return f'Отзывы участников'

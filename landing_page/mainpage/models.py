import enum

from django.db import models
from django.utils.timezone import now


class Curators(models.Model):
    class Meta:
        verbose_name_plural = 'Кураторы'

    def __str__(self) -> str:
        return f'Куратор {self.curator_name}'

    curator_name = models.CharField(
        max_length=50,
        verbose_name='Имя и фамилия куратора',
        help_text='Сначала имя, потом фамилия'
    )

    curator_bio = models.TextField(
        verbose_name='Биография куратора',
        help_text='Где и кем работает, что программирует'
    )

    curator_photo = models.ImageField(
        help_text='Фотография куратора',
        verbose_name='Фото куратора',
        blank=True,
        upload_to='courators/'
    )

    is_visible = models.BooleanField(
        verbose_name="Показывать на главной",
        default=True,
    )


class GraduateProjects(models.Model):
    class Meta:
        verbose_name_plural = 'LearnPython Проекты Учеников'

    def __str__(self) -> str:
        return f'Проект "{self.project_name}"'

    project_name = models.CharField(
        verbose_name='Название проекта',
        max_length=150,
        help_text='Название проекта',
        default=None
    )

    project_image = models.ImageField(
        verbose_name='Пример интерфейса',
        help_text="Пример интерфейса проекта",
        default=None,
        upload_to='projects/'
    )


class EnrollmentType(enum.StrEnum):
    BASE = "BASE"
    ADVANCED = "ADVANCED"

    @classmethod
    def get_choices(cls) -> list[tuple[str, str]]:
        return [(v, v) for v in cls]


class Enrollment(models.Model):
    timepad_event_id = models.CharField(max_length=64, null=True, blank=True)
    platim_url = models.CharField(max_length=254, null=True, blank=True)

    type = models.CharField(max_length=10, choices=EnrollmentType.get_choices(), null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    end_registration_date = models.DateField()
    early_price_rub = models.IntegerField()
    late_price_rub = models.IntegerField()
    early_price_date_to = models.DateField()
    late_price_date_from = models.DateField()

    @staticmethod
    def get_enrollment_with_active_registration(enrollment_type: EnrollmentType) -> "Enrollment | None":
        return Enrollment.objects.filter(
            type=enrollment_type,
            end_registration_date__gte=now(),
        ).first()

    def __str__(self) -> str:
        return f"{self.type.capitalize() if self.type else 'NO TYPE'} enrollment ({self.start_date} - {self.end_date})"


class CourseReview(models.Model):
    title = models.CharField(max_length=254)
    text = models.TextField()
    review_for = models.CharField(max_length=10, choices=EnrollmentType.get_choices(), null=True, blank=True)
    reviewer_name = models.CharField(max_length=254, null=True, blank=True)
    reviewed_at = models.DateField()

    def __str__(self) -> str:
        return f'{self.title} ({self.review_for})'

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from movies.mixins import TimeStampedMixin, UUIDMixin


class Genre(UUIDMixin, TimeStampedMixin):
    genre_name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True)

    class Meta:
        db_table = "genre"
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.genre_name


class GenreFilmwork(UUIDMixin, TimeStampedMixin):
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)

    class Meta:
        db_table = "genre_film_work"
        verbose_name = 'Жанр фильма'
        verbose_name_plural = 'Жанры фильма'


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.TextField(_('full_name'), blank=False, max_length=255)

    class Meta:
        db_table = "person"
        verbose_name = 'Персонаж'
        verbose_name_plural = 'Персонажи'

    def __str__(self):
        return self.full_name


class Filmwork(UUIDMixin, TimeStampedMixin):
    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'),
                                   blank=True, max_length=255)
    creation_date = models.DateField(_('creation_date'),
                                     auto_now_add=True, blank=True)
    rating = models.FloatField(_('rating'), blank=True,
                               validators=[MinValueValidator(0),
                                           MaxValueValidator(100)])
    genres = models.ManyToManyField(Genre, through='GenreFilmwork')
    persons = models.ManyToManyField(Person, through="PersonFilmWork")

    class Meta:
        db_table = "film_work"
        verbose_name = 'Кинопроизведение'
        verbose_name_plural = 'Кинопроизведения'
        indexes = [
            models.Index(fields=['creation_date'],
                         name='film_work_creation_date_idx')
        ]

    def __str__(self):
        return self.title

    class FilmworkType(models.TextChoices):
        MOVIE = "movie", _("movie")
        TV_SHOW = "tv_show", _("tv_show")
    type = models.CharField(_('type'), max_length=255,
                            choices=FilmworkType.choices, blank=False)


class PersonFilmwork(UUIDMixin, TimeStampedMixin):
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    person = models.ForeignKey('Person', on_delete=models.CASCADE)

    class Meta:
        db_table = "person_film_work"
        verbose_name = 'Кинопроизведение персонажа'
        verbose_name_plural = 'Кинопроизведения персонажа'
        indexes = [
            models.Index(fields=['film_work_id', 'person_id', 'role'],
                         name='film_work_person_id_role')
        ]

    class RoleType(models.TextChoices):
        DIRECTOR = "режисер", _("director")
        PRODUCER = "продюсер", _("producer")
        ACTOR = "актер", _("actor")

    role = models.TextField(_('role'), max_length=255,
                            choices=RoleType.choices, blank=False)

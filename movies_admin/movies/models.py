import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    def __str__(self):
        return self.name
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True)

    class Meta:
        db_table = "genre"
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class GenreFilmwork(UUIDMixin, TimeStampedMixin):
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)

    class Meta:
        db_table = "genre_film_work"
        verbose_name = 'Жанр фильма'
        verbose_name_plural = 'Жанры фильма'


class Filmwork(UUIDMixin, TimeStampedMixin):
    def __str__(self):
        return self.title
    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'),
                                   blank=True, max_length=255)
    creation_date = models.DateField(_('creation_date'),
                                     auto_now_add=True, blank=True)
    rating = models.FloatField(_('rating'), blank=True,
                               validators=[MinValueValidator(0),
                                           MaxValueValidator(100)])
    genres = models.ManyToManyField(Genre, through='GenreFilmwork')

    class FilmworkType(models.TextChoices):
        MOVIE = "movie", _("movie")
        TV_SHOW = "tv_show", _("tv_show")
    type = models.CharField(_('type'), max_length=255,
                            choices=FilmworkType.choices, blank=False)

    class Meta:
        db_table = "film_work"
        verbose_name = 'Кинопроизведение'
        verbose_name_plural = 'Кинопроизведения'


class Person(UUIDMixin, TimeStampedMixin):
    def __str__(self):
        return self.full_name
    full_name = models.TextField(_('full_name'), blank=False, max_length=255)

    class Meta:
        db_table = "person"
        verbose_name = 'Персонаж'
        verbose_name_plural = 'Персонажи'


class PersonFilmwork(UUIDMixin, TimeStampedMixin):
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    role = models.TextField(_('role'))

    class Meta:
        db_table = "person_film_work"
        verbose_name = 'Кинопроизведение персонажа'
        verbose_name_plural = 'Кинопроизведения персонажа'

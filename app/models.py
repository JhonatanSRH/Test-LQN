from django.db import models
from model_utils.models import TimeStampedModel
from enum import Enum


class SimpleNameModel(models.Model):
    name = models.CharField(max_length=128)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Planet(TimeStampedModel, SimpleNameModel):
    """ Planetas del universo de Star Wars """

    rotation_period = models.CharField(max_length=40, blank=True)
    orbital_period = models.CharField(max_length=40, blank=True)
    diameter = models.CharField(max_length=40, blank=True)
    climate = models.CharField(max_length=40, blank=True)
    gravity = models.CharField(max_length=40, blank=True)
    terrain = models.CharField(max_length=40, blank=True)
    surface_water = models.CharField(max_length=40, blank=True)
    population = models.CharField(max_length=40, blank=True)

    class Meta:
        db_table = 'planet'

class GenderEnum(Enum):
    """ Opciones de genero para los Personajes """
    MALE = 'male'
    FEMALE = 'female'
    HERMAPHRODITE = 'hermaphrodite'
    NA = 'n/a'

    @classmethod
    def choices(cls):
        return tuple((x, x) for x in cls)
class People(TimeStampedModel, SimpleNameModel):
    """ Personajes del universo de Star Wars """
    
    HAIR_OPTIONS = [
        ('black', 'black'), 
        ('brown', 'brown'), 
        ('blond', 'blonde'), 
        ('red', 'red'), 
        ('white', 'white'), 
        ('bald', 'bald')
    ]
    EYE_OPTIONS = [
        ('black', 'black'), 
        ('brown', 'brown'), 
        ('yellow', 'YELLOW'), 
        ('red', 'red'), 
        ('green', 'green'), 
        ('purple', 'purple'), 
        ('unknown', 'unknown')
    ]
    # GENDER_OPTIONS = [
    #     ('male', 'MALE'), 
    #     ('female', 'FEMALE'), 
    #     ('hermaphrodite', 'HERMAPHRODITE'), 
    #     ('n/a', 'NA')
    # ]
    height = models.CharField(max_length=16, blank=True)
    mass = models.CharField(max_length=16, blank=True)
    hair_color = models.CharField(max_length=32, blank=True, choices=HAIR_OPTIONS)
    skin_color = models.CharField(max_length=32, blank=True)
    eye_color = models.CharField(max_length=32, blank=True, choices=EYE_OPTIONS)
    birth_year = models.CharField(max_length=16, blank=True)
    gender = models.CharField(max_length=64, blank=True, choices=GenderEnum.choices())
    home_world = models.ForeignKey(Planet, on_delete=models.CASCADE, related_name='inhabitants')

    class Meta:
        db_table = 'people'
        verbose_name_plural = 'people'


class Director(SimpleNameModel):
    """ Directores de pel??culas"""

    class Meta:
        db_table = 'director'


class Producer(SimpleNameModel):
    """ Productores de pel??culas"""

    class Meta:
        db_table = 'producer'


class Film(TimeStampedModel):
    title = models.CharField(max_length=100)
    episode_id = models.PositiveSmallIntegerField()
    opening_crawl = models.TextField(max_length=1000)
    release_date = models.DateField()
    director = models.ForeignKey(Director, on_delete=models.CASCADE, related_name='films')
    producer = models.ManyToManyField(Producer, related_name='films')
    characters = models.ManyToManyField(People, related_name='films', blank=True)
    planets = models.ManyToManyField(Planet, related_name='films', blank=True)

    class Meta:
        db_table = 'film'

    def __str__(self):
        return self.title

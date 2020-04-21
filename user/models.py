from django.db import models
from django.contrib.auth.models import User


class SkillCategory(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()

    class Meta:
        verbose_name_plural = 'SkillCategories'


class Skill(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    category = models.ForeignKey(SkillCategory, on_delete=models.CASCADE)
    rating = models.FloatField(default=0)
    status = models.CharField(max_length=32, default='learn')


class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=64)
    birth_date = models.DateField()
    availability = models.CharField(max_length=256)
    reviews = models.TextField()
    skills = models.ManyToManyField(Skill, blank=True)
    status = models.CharField(max_length=32, default='user')
    rating = models.IntegerField(default=0)

from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()

    class Meta:
        verbose_name_plural = 'Categories'


class Skill(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)


class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=64)
    birth_date = models.DateField()
    availability = models.CharField(max_length=256)
    reviews = models.TextField()
    rating = models.FloatField(default=0)
    skills = models.ManyToManyField(Skill, blank=True)
    friends = models.ManyToManyField('self', through='Friends', symmetrical=False,
                                     related_name='friend_with', blank=True)
    relationships = models.ManyToManyField('self', through='Relationship', symmetrical=False,
                                           related_name='related_to', blank=True)


class Relationship(models.Model):
    LEARN = "L"
    TEACH = "T"
    PARTNER = "P"

    SkillStatus = (
        (LEARN, "learn"),
        (TEACH, "teach"),
        (PARTNER, "partner"),
    )

    from_person = models.ForeignKey(Person, related_name='from+', on_delete=models.CASCADE)
    to_person = models.ForeignKey(Person, related_name='to+', on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    status = models.CharField(max_length=2, choices=SkillStatus, default=LEARN)
    rating = models.FloatField(default=0)


class Friends(models.Model):
    from_person = models.ForeignKey(Person, related_name='from_people', on_delete=models.CASCADE)
    to_person = models.ForeignKey(Person, related_name='to_people', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Friends'

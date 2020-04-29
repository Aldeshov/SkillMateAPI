from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Rating(models.Model):
    mark = models.FloatField(default=0, validators=[MaxValueValidator(5), MinValueValidator(0)])
    count = models.IntegerField(default=0)


class Data(models.Model):
    photo = models.FileField(upload_to='data_photos', blank=True)
    about = models.TextField()


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
    about_me = models.TextField(blank=True)
    avatar = models.FileField(upload_to='avatars', blank=True)

    rating = models.OneToOneField(Rating, on_delete=models.CASCADE)
    portfolio = models.ManyToManyField(Data, blank=True)
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

    from_person = models.ForeignKey(Person, related_name='from_related', on_delete=models.CASCADE)
    to_person = models.ForeignKey(Person, related_name='to_related', on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    status = models.CharField(max_length=2, choices=SkillStatus, default=LEARN)


class SkillRating(models.Model):
    rating = models.FloatField(default=1,  validators=[MaxValueValidator(5), MinValueValidator(1)])
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    from_person = models.ForeignKey(Person, related_name='from_rated', on_delete=models.CASCADE)
    to_person = models.ForeignKey(Person, related_name='to_rated', on_delete=models.CASCADE)


class Friends(models.Model):
    from_person = models.ForeignKey(Person, related_name='from_friend', on_delete=models.CASCADE)
    to_person = models.ForeignKey(Person, related_name='to_friend', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Friends'

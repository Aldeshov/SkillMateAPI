from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


'''
This model for Rating. It has fields: mark, count. Mark is average number. Count is a number for rating
'''


class Rating(models.Model):
    mark = models.FloatField(default=0, validators=[MaxValueValidator(5), MinValueValidator(0)])
    count = models.IntegerField(default=0)


'''
This model for Data. It is a profile that has photo and information about user
'''


class Data(models.Model):
    photo = models.FileField(upload_to='data_photos', blank=True)
    about = models.TextField()


# This model for Category. It has fields:name, description
class Category(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()

    class Meta:
        verbose_name_plural = 'Categories'


# This model for Skill. It has fields: name, description, category, created_by.
# Created_by is a foreign key for User. It makes relation which useful for requests
class Skill(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)


# This model for Person.  User is a OneToOne field.
# A OneToOneField is essentially the same as a ForeignKey,
# with the exception that it always carries a "unique" constraint.
# Skills,friends are ManyToManyField .Provide a many-to-many relation by using an intermediary model
# that holds two ForeignKey fields pointed at the two sides of the relation.
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


# This model for relationship . It has three foreign keys, which are provide connection with Person and Skill.
# It makes relations between persons by status. For instance: field from_person and to_person are for status by
# which we can understand who does what, for example: learn, teach or partnership
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


# This model is needed for a  RelationShip model by which the teacher’s grade is determined
class SkillRating(models.Model):
    rating = models.FloatField(default=1,  validators=[MaxValueValidator(5), MinValueValidator(1)])
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    from_person = models.ForeignKey(Person, related_name='from_rated', on_delete=models.CASCADE)
    to_person = models.ForeignKey(Person, related_name='to_rated', on_delete=models.CASCADE)


# This model for Friends. It has two foreign keys, which are provide relation with Person
class Friends(models.Model):
    from_person = models.ForeignKey(Person, related_name='from_friend', on_delete=models.CASCADE)
    to_person = models.ForeignKey(Person, related_name='to_friend', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Friends'

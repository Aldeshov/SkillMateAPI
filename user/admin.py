from django.contrib import admin

from .models import Category, Skill, Person, Relationship, Friends, Rating, Data, SkillRating

admin.site.register(Category)
admin.site.register(Skill)
admin.site.register(Person)
admin.site.register(Relationship)
admin.site.register(Rating)
admin.site.register(SkillRating)
admin.site.register(Data)
admin.site.register(Friends)

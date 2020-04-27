from django.contrib import admin

from .models import Category, Skill, Person, Relationship, Friends

admin.site.register(Category)
admin.site.register(Skill)
admin.site.register(Person)
admin.site.register(Relationship)
admin.site.register(Friends)

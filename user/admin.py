from django.contrib import admin

from .models import SkillCategory, Skill, Person

admin.site.register(SkillCategory)
admin.site.register(Skill)
admin.site.register(Person)

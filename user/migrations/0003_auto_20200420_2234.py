# Generated by Django 2.2.12 on 2020-04-20 16:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20200420_2053'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='skill',
            name='category',
        ),
        migrations.RemoveField(
            model_name='skillmate',
            name='person',
        ),
        migrations.RemoveField(
            model_name='skillmate',
            name='skills',
        ),
        migrations.DeleteModel(
            name='Person',
        ),
        migrations.DeleteModel(
            name='Skill',
        ),
        migrations.DeleteModel(
            name='SkillCategory',
        ),
        migrations.DeleteModel(
            name='SkillMate',
        ),
    ]

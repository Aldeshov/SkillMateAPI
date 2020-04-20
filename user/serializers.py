from rest_framework import serializers

from user.models import SkillCategory, Skill, Person
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')


class SkillCategorySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = SkillCategory
        fields = ('id', 'name', 'description')


class SkillSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    category = SkillCategorySerializer(many=False, read_only=True)
    category_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Skill
        fields = ('id', 'name', 'description', 'category', 'category_id', 'rating', 'status')


class PersonSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user = UserSerializer(many=False, read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    skills = SkillSerializer(many=True, read_only=True)

    class Meta:
        model = Person
        fields = ('id', 'user', 'user_id', 'gender', 'birth_date', 'availability',
                  'reviews', 'skills', 'status', 'rating')

from rest_framework import serializers

from user.models import Category, Skill, Person, Relationship, Data
from django.contrib.auth.models import User


class DataSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    photo = serializers.FileField()
    about = serializers.CharField()

    class Meta:
        model = Data
        fields = ('id', 'photo', 'about')


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')


class CategorySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'description')


class SkillSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    category = CategorySerializer(many=False, read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    created_by = UserSerializer(read_only=True, many=False)
    created_by_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Skill
        fields = ('id', 'name', 'description', 'category', 'category_id', 'created_by', 'created_by_id')


class PersonSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user = UserSerializer(many=False, read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    rating_id = serializers.IntegerField(write_only=True)
    avatar = serializers.FileField()

    class Meta:
        model = Person
        fields = ('id', 'user', 'user_id', 'gender', 'birth_date', 'availability',
                  'reviews', 'about_me', 'avatar', 'rating_id')


class RelationshipSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    skill = SkillSerializer(many=False, read_only=True)
    skill_id = serializers.IntegerField(write_only=True)
    from_person_id = serializers.IntegerField(write_only=True)
    to_person = PersonSerializer(read_only=True, many=False)
    to_person_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Relationship
        fields = ('id', 'status', 'skill', 'skill_id', 'from_person_id', 'to_person', 'to_person_id')


from django.contrib.auth.models import User
from django.shortcuts import render

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from user.serializers import SkillCategorySerializer, SkillSerializer, PersonSerializer, UserSerializer
from user.models import SkillCategory, Skill, Person


@api_view(['GET', 'POST'])
def list_of_users(request):
    if request.method == 'GET':
        users = Person.objects.all()
        serializer = PersonSerializer(users, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        user = request.data.get("user")
        u_serializer = UserSerializer(data=user)
        if u_serializer.is_valid():
            u_serializer.save()
        else:
            return Response({'error': u_serializer.errors}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        try:
            person = request.data
            user_id = User.objects.get(username=request.data.get("user")['username']).id
            person['user_id'] = user_id
        except Exception as e:
            return Response({"error": e})
        p_serializer = PersonSerializer(data=person)
        if p_serializer.is_valid():
            p_serializer.save()
            for s in request.data.get("skills"):
                skill = Skill.objects.get(id=s.get("id"))
                Person.objects.get(user_id=user_id).skills.add(skill)
            return Response(p_serializer.data, status=status.HTTP_201_CREATED)
        return Response({'error': p_serializer.errors}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#               Sample POST Request For Person
# {
#     "user": {
#         "username": "new_username",
#         "first_name": "new_first_name",
#         "last_name": "new_last_name",
#         "email": "newemail@example.dot"
#     },
#     "gender": "male",
#     "birth_date": "2020-04-05",
#     "availability": "sample",
#     "reviews": "Reviews",
#     "skills": [
#         {
#             "id": 1
#         },
#         {
#             "id": 2
#         }
#     ],
#     "status": "Person",
#     "rating": 3
# }


@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, user_id):
    try:
        person = Person.objects.get(id=user_id)
    except User.DoesNotExist as e:
        return Response({'error': str(e)})

    if request.method == 'GET':
        serializer = PersonSerializer(person)
        return Response(serializer.data)

    elif request.method == 'PUT':
        if not request.data:
            return Response({"null": "Empty JSON"}, status=status.HTTP_400_BAD_REQUEST)
        if request.data.get("user"):
            user = User.objects.get(id=person.user.id)
            data = request.data.get("user")
            data["username"] = request.data.get("user").get("username") or user.username
            serializer = UserSerializer(instance=user, data=data)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response({'error': serializer.errors})
        data = request.data
        if request.data.get("user"):
            data["user_id"] = request.data.get("user").get("user_id") or person.user.id
        else:
            data["user_id"] = person.user.id
        data["birth_date"] = request.data.get("birth_date") or person.birth_date
        data["availability"] = request.data.get("availability") or person.availability
        data["reviews"] = request.data.get("reviews") or person.reviews

        serializer = PersonSerializer(instance=person, data=data)
        if serializer.is_valid():
            serializer.save()
            if request.data.get("skills"):
                person.skills.clear()
                for s in request.data.get("skills"):
                    skill = Skill.objects.get(id=s.get("id"))
                    person.skills.add(skill)
            return Response(serializer.data)
        return Response({'error': serializer.errors})

    elif request.method == 'DELETE':
        user = User.objects.get(id=person.user.id)
        person.delete()
        user.delete()
        return Response({'deleted': True})


# @api_view(['GET', 'POST'])
# def list_of_skills(request):
#     if request.method == 'GET':
#         skills = Skill.objects.all()
#         serializer = SkillSerializer(skills, many=True)
#         return Response(serializer.data)
#
#     elif request.method == 'POST':
#         serializer = SkillSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response({'error': serializer.errors},
#                         status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#
#
# @api_view(['GET', 'PUT', 'DELETE'])
# def skill_detail(request, skill_id):
#     try:
#         skill = Skill.objects.get(id=skill_id)
#     except User.DoesNotExist as e:
#         return Response({'error': str(e)})
#
#     if request.method == 'GET':
#         serializer = SkillSerializer(skill)
#         return Response(serializer.data)
#
#     elif request.method == 'PUT':
#         serializer = SkillSerializer(instance=skill, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response({'error': serializer.errors})
#
#     elif request.method == 'DELETE':
#         skill.delete()
#         return Response({'deleted': True})
#
#
# @api_view(['GET'])
# def users_by_skill(request, skill_id):
#     try:
#         users = User.objects.filter(skill=Skill.objects.get(id=skill_id))
#     except Skill.DoesNotExist as e:
#         return Response({'error': str(e)})
#     if request.method == "GET":
#         serializer = UserSerializer(data=users, many=True)
#         if serializer.is_valid():
#             serializer.save()
#         return Response(serializer.data)
#
#
# @api_view(['GET'])
# def user_by_status(request, st_id):
#     users = User.objects.all()
#     users_by_status = []
#     for x in users:
#         if x.status == st_id:
#             users_by_status.append(x)
#
#     serializer = UserSerializer(data=users_by_status, many=True)
#     if serializer.is_valid():
#         serializer.save()
#     return Response(serializer.data)
#
#
# @api_view(['GET'])
# def user_top(request):
#     users = User.objects.all().order_by('-rait')
#     serializer = UserSerializer(data=users, many=True)
#     if serializer.is_valid():
#         serializer.save()
#     return Response(serializer.data[0:10])
#
#
# @api_view(['GET'])
# def skill_top(request):
#     skills = Skill.objects.all().order_by('-raiting')
#     serializer = SkillSerializer(data=skills, many=True)
#     if serializer.is_valid():
#         serializer.save()
#     return Response(serializer.data[0:10])
#
#
# @api_view(['GET'])
# def skill_for_st(request, st_id):
#     skills = Skill.objects.filter(status=st_id)
#     serializer = SkillSerializer(data=skills, many=True)
#     if serializer.is_valid():
#         serializer.save()
#     return Response(serializer.data)



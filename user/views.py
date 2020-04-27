from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from user.serializers import CategorySerializer, SkillSerializer, \
    PersonSerializer, UserSerializer, RelationshipSerializer
from user.models import Category, Skill, Person, Relationship, Friends


@api_view(['GET', 'PUT', 'DELETE'])
def current_user(request):
    try:
        person = Person.objects.get(user=request.user)
        user = User.objects.get(id=person.user.id)
    except Exception as e:
        return Response({'error': str(e)})

    if request.method == 'GET':
        if request.method == 'GET':
            serializer = PersonSerializer(person)
            return Response(serializer.data)

    elif request.method == 'PUT':
        data = request.data
        if data.get("user"):
            user_data = data.pop("user")
            user_data["username"] = user_data.get("username") or user.username
            serializer = UserSerializer(instance=user, data=user)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response({'error': serializer.errors})
        data["user_id"] = user.id
        data["gender"] = data.get("gender") or person.gender
        data["birth_date"] = data.get("birth_date") or person.birth_date
        data["availability"] = data.get("availability") or person.availability
        data["reviews"] = data.get("reviews") or person.reviews

        serializer = PersonSerializer(instance=person, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({'error': serializer.errors})

    elif request.method == 'DELETE':
        person.delete()
        user.delete()
        return Response({'deleted': True})


@api_view(['GET', 'PUT', 'DELETE'])
def current_user_friends(request):
    try:
        person = Person.objects.get(user=request.user)
    except Exception as e:
        return Response({'error': str(e)})

    if request.method == 'GET':
        friends = person.friends.filter(to_people__from_person=person)
        serializer = PersonSerializer(friends, many=True)
        return Response(serializer.data)

    if request.method == 'PUT':
        friend_id = request.data.get("person_id")
        Friends.objects.get_or_create(from_person=person, to_person=Person.objects.get(id=friend_id))
        return Response({"Created": True}, status=status.HTTP_200_OK)

    if request.method == 'DELETE':
        friend_id = request.data.get("person_id")
        friend1 = Friends.objects.get(from_person=person, to_person=Person.objects.get(id=friend_id))
        friend1.delete()
        return Response({"Deleted": True}, status=status.HTTP_200_OK)


@api_view(['GET', 'PUT', 'DELETE'])
def current_user_skills(request):
    try:
        person = Person.objects.get(user=request.user)
    except Exception as e:
        return Response({'error': str(e)})

    if request.method == 'GET':
        skills = person.skills.all()
        serializer = SkillSerializer(skills, many=True)
        return Response(serializer.data)

    if request.method == 'PUT':
        skill_id = request.data.get("skill_id")
        person.skills.add(Skill.objects.get(id=skill_id))
        return Response({"Created": True}, status=status.HTTP_200_OK)

    if request.method == 'DELETE':
        skill_id = request.data.get("skill_id")
        skill = person.skills.all().get(id=skill_id)
        skill.delete()
        return Response({"Deleted": True}, status=status.HTTP_200_OK)


@api_view(['GET', 'PUT', 'DELETE'])
def current_user_relationships(request):
    try:
        person = Person.objects.get(user=request.user)
    except Exception as e:
        return Response({'error': str(e)})

    if request.method == 'GET':
        relationships = Relationship.objects.filter(from_person=person)
        serializer = RelationshipSerializer(relationships, many=True)
        return Response(serializer.data)

    if request.method == 'PUT':
        data = request.data
        data['from_person_id'] = person.id
        serializer = RelationshipSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Created": True}, status=status.HTTP_200_OK)
        return Response({"error": serializer.errors})

    if request.method == 'DELETE':
        relationship_id = request.data.get("relationship_id")
        rel = Relationship.objects.get(id=relationship_id)
        rel.delete()
        return Response({"Deleted": True}, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def list_of_users(request):
    if request.method == 'GET':
        users = Person.objects.all()
        serializer = PersonSerializer(users, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = request.data
        user = data.pop("user")
        u_serializer = UserSerializer(data=user)
        if u_serializer.is_valid():
            u_serializer.save()
            person = data
            person['user_id'] = u_serializer.data.get("id")
            p_serializer = PersonSerializer(data=person)
            if p_serializer.is_valid():
                p_serializer.save()
                skills = data.pop("skills")
                for s in skills:
                    try:
                        p = Person.objects.get(id=p_serializer.data.get("id"))
                        p.skills.add(Skill.objects.get(id=s))
                        p.save()
                    except Exception as e:
                        print("ERROR: " + str(e))
                return Response(p_serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'POST'])
def category_list(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({'error': serializer.errors}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def user_detail(request, user_id):
    try:
        person = Person.objects.get(id=user_id)
    except Person.DoesNotExist as e:
        return Response({'error': str(e)})

    if request.method == 'GET':
        serializer = PersonSerializer(person)
        return Response(serializer.data)


@api_view(['GET'])
def user_friends(request, user_id):
    try:
        person = Person.objects.get(id=user_id)
    except User.DoesNotExist as e:
        return Response({'error': str(e)})

    if request.method == 'GET':
        friends = person.friends.filter(
            to_people__from_person=person)
        serializer = PersonSerializer(friends, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def user_skills(request, user_id):
    try:
        person = Person.objects.get(id=user_id)
    except User.DoesNotExist as e:
        return Response({'error': str(e)})

    if request.method == 'GET':
        skills = person.skills.all()
        serializer = SkillSerializer(skills, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def category_skills(request, category_id):
    if request.method == 'GET':
        skills = [s for s in Skill.objects.all() if s.category.id == category_id]
        serializer = SkillSerializer(skills, many=True)
        return Response(serializer.data)


@api_view(['GET', 'POST'])
def list_of_skills(request):
    if request.method == 'GET':
        skills = Skill.objects.all()
        serializer = SkillSerializer(skills, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        if Category.objects.get(id=request.data.get("category_id")):
            data = request.data
            data["created_by_id"] = request.user.id
            serializer = SkillSerializer(data=data)
        else:
            return Response({"null": "Category Not Found"}, status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'error': serializer.errors}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'PUT', 'DELETE'])
def category_detail(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist as e:
        return Response({'error': str(e)})

    if request.method == 'GET':
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CategorySerializer(instance=category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({'error': serializer.errors})

    elif request.method == 'DELETE':
        category.delete()
        return Response({'deleted': True})


@api_view(['GET', 'PUT', 'DELETE'])
def skill_detail(request, skill_id):
    try:
        skill = Skill.objects.get(id=skill_id)
    except User.DoesNotExist as e:
        return Response({'error': str(e)})

    if request.method == 'GET':
        serializer = SkillSerializer(skill)
        return Response(serializer.data)

    elif request.method == 'PUT':
        if Category.objects.check(id=request.data.get("category_id")):
            data = request.data
            data["created_by_id"] = skill.created_by.id
            serializer = SkillSerializer(instance=skill, data=data)
        else:
            return Response({"null": "Category Not Found"}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({'error': serializer.errors})

    elif request.method == 'DELETE':
        skill.delete()
        return Response({'deleted': True})


@api_view(['GET'])
def users_by_skill(request, skill_id):
    try:
        persons = [p for p in Person.objects.all() if len(p.skills.filter(id=skill_id)) >= 1]
    except Skill.DoesNotExist as e:
        return Response({'error': str(e)})

    if request.method == "GET":
        serializer = PersonSerializer(persons, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def user_top(request):
    if request.method == "GET":
        persons = Person.objects.all().order_by('-rating')[:10]
        serializer = PersonSerializer(persons, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def skill_top(request):
    if request.method == "GET":
        skills = Skill.objects.all().order_by('-rating')[:10]
        serializer = SkillSerializer(skills, many=True)
        return Response(serializer.data)

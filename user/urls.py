from django.urls import path, re_path
from rest_framework_jwt.views import obtain_jwt_token

from user.views import list_of_users, user_detail, list_of_skills, skill_detail, category_detail, \
    user_friends, users_by_skill, user_top, skill_top, category_skills, category_list, \
    user_skills, current_user, current_user_friends, current_user_skills, current_user_relationships


urlpatterns = [
    path('login', obtain_jwt_token),
    path('users', list_of_users),
    path('users/current', current_user),
    path('users/current/friends', current_user_friends),
    path('users/current/skills', current_user_skills),
    path('users/current/relationships', current_user_relationships),
    path('users/<int:user_id>', user_detail),
    path('users/<int:user_id>/friends', user_friends),
    path('users/<int:user_id>/skills', user_skills),
    path('skills', list_of_skills),
    path('skills/<int:skill_id>', skill_detail),
    path('skills/<int:skill_id>/users', users_by_skill),  # people who has special skill
    path('categories', category_list),
    path('categories/<int:category_id>', category_detail),
    path('categories/<int:category_id>/skills', category_skills),
    path('users/top_ten', user_top),
    path('skills/top_ten', skill_top),
]

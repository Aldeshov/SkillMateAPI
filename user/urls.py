from django.urls import path, re_path

from user.views import list_of_users, user_detail, list_of_skills, skill_detail, category_detail, \
    users_by_skill, user_by_status, user_top, skill_top, skills_by_status, category_skills, category_list

urlpatterns = [
    path('users/', list_of_users),
    path('users/<int:user_id>/', user_detail),
    path('skills/', list_of_skills),
    path('skills/<int:skill_id>/', skill_detail),
    path('skills/<int:skill_id>/users/', users_by_skill),  # people who has special skill
    path('categories/', category_list),
    path('categories/<int:category_id>/', category_detail),
    path('categories/<int:category_id>/skills', category_skills),
    path('users/<str:_status>/', user_by_status),
    path('users/top_ten', user_top),
    path('skills/top_ten', skill_top),
    path('skills/<str:_status>', skills_by_status),
]

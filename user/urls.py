from django.urls import path, re_path

from user.views import list_of_users, user_detail
# , list_of_skills, skill_detail, users_by_skill, user_by_status, \
# user_top, skill_top, skill_for_st

urlpatterns = [
    path('users/', list_of_users),
    path('users/<int:user_id>/', user_detail),

    # path('skills/', list_of_skills),
    # path('skills/<int:skill_id>/', skill_detail),
    # path('skills/<int:skill_id>/users/', users_by_skill),  # people who has special skill
    # path('users/<str:st_id>/', user_by_status),
    # path('users/top_ten', user_top),
    # path('skills/top_ten', skill_top),
    # path('skills/<str:st_id>', skill_for_st),
]

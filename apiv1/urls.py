from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

from .views import ProfileCreateView, SubjectCreateView, SubjectListView, SubjectUpdateView, SubjectDeleteView, \
    ProfileListView, TeamListView, NotGroupedProfileListView, TeamCreateView

urlpatterns = [
    path('signup/', ProfileCreateView.as_view()),
    path('login/', obtain_auth_token),
    path('subject/create/', SubjectCreateView.as_view()),
    path('subject/list/', SubjectListView.as_view()),
    path('subject/update/<int:pk>', SubjectUpdateView.as_view()),
    path('subject/delete/<int:pk>', SubjectDeleteView.as_view()),
    path('profile/list/all/', ProfileListView.as_view()),
    path('profile/list/single/', NotGroupedProfileListView.as_view()),
    path('team/list/', TeamListView.as_view()),
    path('team/create/', TeamCreateView.as_view()),

]

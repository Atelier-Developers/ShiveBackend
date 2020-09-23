from django.urls import path, include
from rest_framework.authtoken.views import ObtainAuthToken
from .permissions import IsAlive

from .views import ProfileCreateView, SubjectCreateView, SubjectListView, SubjectUpdateView, SubjectDeleteView, \
    ProfileListView, TeamListView, NotGroupedProfileListView, TeamCreateView, RemoveFromListDestroyView, \
    MoveProfileToTeamCreateView, PendingProfileListView, AssignSubjectToTeamCreateView

login = ObtainAuthToken
login.permission_classes = [IsAlive]
Login = login.as_view()

urlpatterns = [
    path('signup/', ProfileCreateView.as_view()),
    path('login/', Login),
    path('subject/create/', SubjectCreateView.as_view()),
    path('subject/list/', SubjectListView.as_view()),
    path('subject/update/<int:pk>', SubjectUpdateView.as_view()),
    path('subject/delete/<int:pk>', SubjectDeleteView.as_view()),
    path('profile/list/all/', ProfileListView.as_view()),
    path('profile/list/pending/', PendingProfileListView.as_view()),
    path('profile/list/single/', NotGroupedProfileListView.as_view()),
    path('profile/move/', MoveProfileToTeamCreateView.as_view()),
    path('team/list/', TeamListView.as_view()),
    path('team/create/', TeamCreateView.as_view()),
    path('team/remove-profile/<int:pk>', RemoveFromListDestroyView.as_view()),
    path('presentation/create/', AssignSubjectToTeamCreateView.as_view()),

]

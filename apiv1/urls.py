from django.urls import path, include
from rest_framework.authtoken.views import ObtainAuthToken
from .permissions import IsAlive

from .views import *

# login = ObtainAuthToken
# # login.permission_classes = [IsAlive]
# Login = login.as_view()

urlpatterns = [
    path('signup/', ProfileCreateView.as_view()),
    path('login/', MyObtainAuthToken.as_view()),
    path('subject/create/', SubjectCreateView.as_view()),
    path('subject/list/all/', SubjectListView.as_view()),
    path('subject/list/remaining/', SubjectRemainingListView.as_view()),
    path('subject/update/<int:pk>', SubjectUpdateView.as_view()),
    path('subject/delete/<int:pk>', SubjectDeleteView.as_view()),
    path('profile/list/all/', ProfileListView.as_view()),
    path('profile/role/', RoleApiView.as_view()),
    path('profile/list/pending/', PendingProfileListView.as_view()),
    path('profile/list/single/', NotGroupedProfileListView.as_view()),
    path('profile/move/', MoveProfileToTeamCreateView.as_view()),
    path('profile/accept/', AcceptProfileCreateView.as_view()),
    path('profile/reject/', DeleteProfileCreateView.as_view()),
    path('profile/presentation/', ProfileTeamPresentationView.as_view()),
    path('team/list/', TeamListView.as_view()),
    path('team/list/<int:pk>', TeamRetrieveView.as_view()),
    path('team/create/', TeamCreateView.as_view()),
    path('team/edit/<int:pk>', TeamEditCreateView.as_view()),
    path('team/delete/<int:pk>', TeamDeleteView.as_view()),
    path('team/remove-profile/<int:pk>', RemoveFromListDestroyView.as_view()),
    path('presentation/create/', PresentationCreateView.as_view()),
    path('presentation/list/all/', PresentationListView.as_view()),
    path('presentation/update/<int:pk>', PresentationUpdateView.as_view()),
    path('presentation/delete/<int:pk>', PresentationDeleteView.as_view()),
    path('presentation/comment/create/<int:pk>', CommentCreateView.as_view()),
    path('presentation/comment/list/<int:pk>', CommentListView.as_view()),
    path('presentation/current/', CurrentPresentationGetView.as_view()),
    path('presentation/archive/', ArchiveListView.as_view()),
    path('presentation/semester/<int:pk>', PresentationBySemesterListView.as_view()),
    path('presentation/rate/<int:pk>', RatingCreateView.as_view()),
    path('presentation/upload/<int:pk>', FileUploadView.as_view()),
    path('semester/list/', SemesterListView.as_view()),
    path('ann/create/', AnnouncementCreateView.as_view()),
    path('ann/upload/<int:pk>', AnnFileUploadView.as_view()),
    path('ann/list/', AnnListVIew.as_view()),
    path('presentation/delete-file/<int:pk>', FileDeleteView.as_view()),
    path('video/comment/create/<int:pk>', VideoCommentCreateView.as_view()),
    path('video/comment/list/<int:pk>', VideoCommentListView.as_view()),
    path('file/<int:pk>', VideoDownloadView.as_view()),
    path('assignment/subjects/all/', AssignmentSubjectListView.as_view()),
    path('assignment/subjects/<int:pk>', AssignmentListView.as_view()),
    path('assignment/create/', AssignmentCreateView.as_view()),
    path('assignment/upload/<int:pk>', AssignmentFileUploadView.as_view()),
    path('issue/create/', IssueCreateView.as_view()),
    path('issue/list/', IssueListView.as_view()),
    path('issue/upload/<int:pk>', IssueFileUploadView.as_view())

]

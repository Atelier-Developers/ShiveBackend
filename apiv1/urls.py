from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

from .views import ProfileCreateView

urlpatterns = [
    path('signup/', ProfileCreateView.as_view()),
    path('login/', obtain_auth_token),

]

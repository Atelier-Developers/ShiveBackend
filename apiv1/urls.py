from django.urls import path, include
from .views import ProfileCreateView

urlpatterns = [
    path('signup/', ProfileCreateView.as_view()),

]

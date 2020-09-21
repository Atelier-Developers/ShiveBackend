from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    student_no = models.IntegerField()
    team = models.ForeignKey("Team", on_delete=models.CASCADE)


class Team(models.Model):
    name = models.CharField(max_length=10, default="team")
    presentation = models.OneToOneField("Presentation", on_delete=models.CASCADE)


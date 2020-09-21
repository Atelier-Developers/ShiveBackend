from django.contrib.auth.models import User
from django.db import models
from django_jalali.db import models as jmodels


# Create your models here.

class Semester(models.Model):
    year = models.CharField(max_length=20)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    student_no = models.IntegerField()
    team = models.ForeignKey("Team", on_delete=models.CASCADE, null=True, blank=True, related_name="profiles")
    is_deleted = models.BooleanField(default=False)


class Team(models.Model):
    name = models.CharField(max_length=10, default="team")
    presentation = models.OneToOneField("Presentation", on_delete=models.CASCADE, related_name="team")


class Subject(models.Model):
    title = models.CharField(max_length=512)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name="subjects")


class Presentation(models.Model):
    subject = models.OneToOneField(Subject, on_delete=models.CASCADE, related_name="Presentation")
    deadline = jmodels.jDateTimeField()

    @property
    def rate(self):
        s = 0
        le = 0
        for i in self.ratings.all():
            le += 1
            s += i.rating
        return s/le


class File(models.Model):
    name = models.CharField(max_length=512)
    link = models.CharField(max_length=1024)
    presentation = models.ForeignKey(Presentation, on_delete=models.CASCADE, related_name="files")


class Comment(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    presentation = models.ForeignKey(Presentation, on_delete=models.CASCADE, related_name="comments")
    date_time = jmodels.jDateTimeField(auto_now_add=True)
    text = models.TextField(max_length=5000)


class Rating(models.Model):
    class Meta:
        unique_together = ["profile", "presentation"]

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    presentation = models.ForeignKey(Presentation, on_delete=models.CASCADE, related_name="ratings")
    rating = models.IntegerField()

from django.contrib.auth.models import User
from django.db import models
from django_jalali.db import models as jmodels


# Create your models here.

class Semester(models.Model):
    year = models.CharField(max_length=20)

    def __str__(self):
        return str(self.year)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    student_no = models.IntegerField()
    phone = models.CharField(max_length=15)
    team = models.ForeignKey("Team", on_delete=models.CASCADE, null=True, blank=True, related_name="profiles")
    is_deleted = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=10, default="team")
    presentation = models.OneToOneField("Presentation", on_delete=models.CASCADE, related_name="team", null=True,
                                        blank=True)

    def __str__(self):
        return str(self.name) + str(self.pk)


class Subject(models.Model):
    title = models.CharField(max_length=512)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name="subjects", null=True)

    def __str__(self):
        return self.title


class Presentation(models.Model):
    subject = models.OneToOneField(Subject, on_delete=models.CASCADE, related_name="presentation")
    deadline = jmodels.jDateTimeField(null=True, blank=True)

    @property
    def rate(self):
        s = 0
        le = 0
        for i in self.ratings.all():
            le += 1
            s += i.rating
        return s / le

    def __str__(self):
        return "Presentation of " + str(self.subject) + " by " + str(self.team)


class File(models.Model):
    name = models.CharField(max_length=512)
    link = models.CharField(max_length=1024)
    presentation = models.ForeignKey(Presentation, on_delete=models.CASCADE, related_name="files")

    def __str__(self):
        return self.name


class Comment(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    presentation = models.ForeignKey(Presentation, on_delete=models.CASCADE, related_name="comments")
    date_time = jmodels.jDateTimeField(auto_now_add=True)
    text = models.TextField(max_length=5000)

    def __str__(self):
        return "Comment from " + str(self.profile) + " on " + str(self.presentation)


class Rating(models.Model):
    class Meta:
        unique_together = ["profile", "presentation"]

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    presentation = models.ForeignKey(Presentation, on_delete=models.CASCADE, related_name="ratings")
    rating = models.IntegerField()

    def __str__(self):
        return "Rating from " + str(self.profile) + " on " + str(self.presentation)

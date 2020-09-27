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
    team = models.ForeignKey("Team", on_delete=models.SET_NULL, null=True, blank=True, related_name="profiles")
    is_deleted = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=10, default="team")
    presentation = models.ForeignKey("Presentation", on_delete=models.SET_NULL, related_name="team", null=True,
                                     blank=True)

    def __str__(self):
        return str(self.name) + str(self.pk)


class Subject(models.Model):
    title = models.CharField(max_length=512)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name="subjects", null=True)

    def __str__(self):
        return self.title


class Presentation(models.Model):
    subject = models.OneToOneField(Subject, on_delete=models.CASCADE, related_name="presentation", null=True,
                                   blank=True)
    deadline = models.DateField(null=True, blank=True)
    description = models.TextField(max_length=100000, null=True, blank=True)

    @property
    def rate(self):
        if not self.ratings.all():
            return 0
        s = 0
        le = 0
        for i in self.ratings.all():
            le += 1
            s += i.rating
        return s / le

    def __str__(self):
        return "Presentation of " + str(self.subject) + " by " + str(self.team.first())


class File(models.Model):
    file = models.FileField()
    name = models.CharField(max_length=512)
    link = models.CharField(max_length=1024, default=" ")
    presentation = models.ForeignKey(Presentation, on_delete=models.CASCADE, related_name="files")

    def __str__(self):
        return self.name


class Comment(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    presentation = models.ForeignKey(Presentation, on_delete=models.CASCADE, related_name="comments")
    date_time = models.DateTimeField(auto_now_add=True)
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


# class Test(models.Model):
#     file = models.FileField()
#     link = models.CharField(default="", max_length=2048)
#
#     def save(self, force_insert=False, force_update=False, using=None,
#              update_fields=None, *args, **kwargs):
#         self.link = "https://cdn.atelier-team.ir/shive/" + str(self.file.name)
#         # self.save()
#         super(Test, self).save(*args, **kwargs)


class Announcement(models.Model):
    title = models.CharField(max_length=1234)
    description = models.TextField(max_length=223456)


class AnnouncementFile(models.Model):
    title = models.CharField(max_length=1234, null=True, blank=True)
    file = models.FileField(null=True, blank=True)
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)

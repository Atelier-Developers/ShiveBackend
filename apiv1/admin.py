from django.contrib import admin

from .models import Profile, Team, Semester, Subject, Presentation, File, Comment, Rating, Announcement, \
    AnnouncementFile, VideoComment, AssignmentSubject, Assignment, AssignmentFile

# Register your models here.

admin.site.register(Profile)
admin.site.register(Team)
admin.site.register(Semester)
admin.site.register(Subject)
admin.site.register(Presentation)
admin.site.register(File)
admin.site.register(Comment)
admin.site.register(Rating)
admin.site.register(Announcement)
admin.site.register(AnnouncementFile)
admin.site.register(VideoComment)
admin.site.register(AssignmentSubject)
admin.site.register(Assignment)
admin.site.register(AssignmentFile)

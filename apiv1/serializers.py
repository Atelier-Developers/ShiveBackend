from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _
from .models import Profile, Team, Semester, Subject, Presentation, File, Comment, Rating, AnnouncementFile, \
    Announcement, VideoComment, Assignment, AssignmentSubject, AssignmentFile, IssueFile, Issue


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["pk", "name", "student_no", "phone", "team"]


class CProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["pk", "name"]


class CommentSerializer(serializers.ModelSerializer):
    profile = CProfileSerializer()

    class Meta:
        model = Comment
        fields = ["pk", "profile", "presentation", "date_time", "text"]


class FileSerializer(serializers.ModelSerializer):
    profile = CProfileSerializer()

    class Meta:
        model = File
        fields = ["pk", "file", "name", 'link', 'size', 'date', 'profile']


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["pk", "name", "student_no", "phone", "password"]

    password = serializers.CharField(max_length=256)


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ["pk", "title"]


class PresentationSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer()
    comments = CommentSerializer(many=True)
    files = FileSerializer(many=True)

    class Meta:
        model = Presentation
        fields = ['pk', 'subject', 'deadline', 'rate', 'description', 'comments', 'files']


class TeamSerializer(serializers.ModelSerializer):
    profiles = ProfileSerializer(many=True)
    presentation = PresentationSerializer()

    class Meta:
        model = Team
        fields = ["pk", "presentation", "profiles"]


class MyAuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField(label=_("Username"))
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class CurrentTeamSerializer(serializers.ModelSerializer):
    profiles = ProfileSerializer(many=True)

    class Meta:
        model = Team
        fields = ["pk", "profiles"]


class CurrentPresentationSerializer(serializers.ModelSerializer):
    team = CurrentTeamSerializer(many=True)
    subject = SubjectSerializer()
    comments = CommentSerializer(many=True)
    files = FileSerializer(many=True)

    class Meta:
        model = Presentation
        fields = ['pk', 'subject', 'deadline', 'rate', 'description', 'comments', 'files', 'team']


class SemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = "__all__"


class AnFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnnouncementFile
        fields = "__all__"


class AnnouncementSerializer(serializers.ModelSerializer):
    files = AnFileSerializer(many=True)

    class Meta:
        model = Announcement
        fields = ['pk', 'title', 'description', 'files']


class VideoCommentSerializer(serializers.ModelSerializer):
    profile = CProfileSerializer()

    class Meta:
        model = VideoComment
        fields = "__all__"


class AssignmentSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignmentSubject
        fields = '__all__'


class AssignmentFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignmentFile
        fields = "__all__"


class AssignmentSerializer(serializers.ModelSerializer):
    profile = CProfileSerializer()
    files = AssignmentFileSerializer(many=True)

    class Meta:
        model = Assignment
        fields = ['pk', 'subject', 'name', 'profile', 'files']


class IssueFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssueFile
        fields = "__all__"


class IssueSerializer(serializers.ModelSerializer):
    files = IssueFileSerializer(many=True)
    profile = CProfileSerializer()

    class Meta:
        model = Issue
        fields = ['pk', 'profile', 'title', 'description', 'files']

from rest_framework import serializers

from .models import Profile, Team, Semester, Subject, Presentation, File, Comment, Rating


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["pk", "name", "student_no", "phone", "team"]


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

    class Meta:
        model = Presentation
        fields = ['pk', 'subject', 'deadline', 'rate']


class TeamSerializer(serializers.ModelSerializer):
    profiles = ProfileSerializer(many=True)
    presentation = PresentationSerializer()

    class Meta:
        model = Team
        fields = ["pk", "presentation", "profiles"]


class CommentSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer

    class Meta:
        model = Comment
        fields = ["pk", "profile", "presentation", "date_time", "text"]

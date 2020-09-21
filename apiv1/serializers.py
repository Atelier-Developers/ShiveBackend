from rest_framework import serializers

from .models import Profile, Team, Semester, Subject, Presentation, File, Comment, Rating


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["name", "student_no", "phone"]


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["name", "student_no", "phone", "password"]

    password = serializers.CharField(max_length=256)


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ["title"]


from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _
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
    presentation = PresentationSerializer()

    class Meta:
        model = Team
        fields = ["pk", "presentation", "profiles"]


class CurrentPresentationSerializer(serializers.ModelSerializer):
    team = CurrentTeamSerializer()
    subject = SubjectSerializer()

    class Meta:
        model = Presentation
        fields = ['pk', 'subject', 'deadline', 'rate', 'team']

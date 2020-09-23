from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Count
from apiv1.permissions import IsAdmin, IsAlive
from .serializers import SignupSerializer, SubjectSerializer, ProfileSerializer, TeamSerializer, PresentationSerializer

from .models import Profile, User, Semester, Subject, Team, Presentation


# Create your views here.


class ProfileCreateView(CreateAPIView):
    serializer_class = SignupSerializer

    def post(self, request, *args, **kwargs):
        try:
            u = User.objects.get(username=request.data.get('student_no'))
            p = Profile.objects.get(user=u)

            return Response({"msg": "user already exists"}, status=status.HTTP_409_CONFLICT)

        except User.DoesNotExist:
            u = User.objects.create_user(username=request.data.get('student_no'))
            u.set_password(request.data.get('password'))
            u.save()
            p = Profile.objects.create(user=u, name=request.data.get('name'), student_no=request.data.get('student_no'),
                                       phone=request.data.get('phone'))

        return Response({"msg": "profile created"}, status=status.HTTP_201_CREATED)


class SubjectCreateView(CreateAPIView):
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticated, IsAdmin, IsAlive]

    def post(self, request, *args, **kwargs):
        serializer = SubjectSerializer(data=request.data)
        if serializer.is_valid():
            s = Semester.objects.last()
            serializer.save(semester=s)

            return Response({"msg": "subject created"}, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response({"msg": "something went wrong"}, status=status.HTTP_400_BAD_REQUEST)


class SubjectListView(ListAPIView):
    serializer_class = SubjectSerializer
    queryset = Subject.objects.filter(semester=Semester.objects.last()).order_by("pk")


class SubjectRemainingListView(ListAPIView):
    serializer_class = SubjectSerializer
    queryset = Subject.objects.filter(semester=Semester.objects.last(), presentation=None).order_by("pk")


class SubjectUpdateView(UpdateAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    lookup_field = "pk"
    permission_classes = [IsAuthenticated, IsAdmin, IsAlive]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.title = request.data.get("title")
        instance.save()
        # serializer = self.get_serializer(instance)
        # serializer.is_valid(raise_exception=True)
        # self.perform_update(serializer)

        return Response({"msg": "subject updated"}, status=status.HTTP_200_OK)


class SubjectDeleteView(DestroyAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    lookup_field = "pk"
    permission_classes = [IsAuthenticated, IsAdmin, IsAlive]

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()

        return Response({"msg": "subject deleted"}, status=status.HTTP_200_OK)


class ProfileListView(ListAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsAlive, IsAdmin]
    queryset = Profile.objects.all()


class NotGroupedProfileListView(ListAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsAlive, IsAdmin]
    queryset = Profile.objects.filter(team=None)


class TeamListView(ListAPIView):
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated, IsAlive]
    queryset = Team.objects.all()


class TeamCreateView(CreateAPIView):
    serializer_class = ProfileSerializer(many=True)
    permission_classes = [IsAuthenticated, IsAlive, IsAdmin]

    def post(self, request, *args, **kwargs):
        team = Team.objects.create()

        for pk in self.request.data:
            p = Profile.objects.get(pk=pk)
            p.team = team
            p.save()

        return Response({"msg": "team created"}, status=status.HTTP_201_CREATED)


class RemoveFromListDestroyView(DestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = "pk"
    permission_classes = [IsAuthenticated, IsAdmin, IsAlive]

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.team = None
        instance.save()

        return Response({"msg": "profile removed from team"}, status=status.HTTP_200_OK)


class MoveProfileToTeamCreateView(CreateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsAdmin, IsAlive]

    def post(self, request, *args, **kwargs):
        print("yay", str(self.request.data)[0])

        if str(self.request.data)[0] == '{':
            p = Profile.objects.get(pk=self.request.data.get("profile"))
            t = Team.objects.get(pk=self.request.data.get("team"))
            p.team = t
            p.save()
        elif str(self.request.data)[0] == '[':
            for i in self.request.data:
                p = Profile.objects.get(pk=i["profile"])
                t = Team.objects.get(pk=i["team"])
                p.team = t
                p.save()

        return Response({"msg": "profile team changed"}, status=status.HTTP_200_OK)


class PendingProfileListView(ListAPIView):
    permission_classes = [IsAdmin, IsAlive, IsAuthenticated]
    serializer_class = ProfileSerializer
    queryset = Profile.objects.filter(is_deleted=True)


class AcceptProfileCreateView(CreateAPIView):
    permission_classes = [IsAdmin, IsAlive, IsAuthenticated]
    serializer_class = ProfileSerializer

    def post(self, request, *args, **kwargs):
        for i in self.request.data:
            p = Profile.objects.get(pk=i)
            p.is_deleted = False
            p.save()

        return Response({"msg": "profiles approved"}, status=status.HTTP_200_OK)


class DeleteProfileCreateView(CreateAPIView):
    permission_classes = [IsAdmin, IsAlive, IsAuthenticated]
    serializer_class = ProfileSerializer

    def post(self, request, *args, **kwargs):
        for i in self.request.data:
            p = Profile.objects.get(pk=i)
            p.delete()

        return Response({"msg": "profiles deleted"}, status=status.HTTP_200_OK)


class PresentationCreateView(CreateAPIView):
    permission_classes = [IsAdmin, IsAlive, IsAuthenticated]
    serializer_class = SubjectSerializer

    def post(self, request, *args, **kwargs):
        t = Team.objects.get(pk=self.request.data.get("team"))
        s = Subject.objects.get(pk=self.request.data.get("subject"))

        p = Presentation.objects.create(subject=s)
        t.presentation = p
        t.save()

        try:
            p.deadline = self.request.data.get("deadline")
            p.save()
        except:
            pass

        return Response({"msg": "presentation created"}, status=status.HTTP_201_CREATED)


class PresentationListView(ListAPIView):
    permission_classes = []
    queryset = Presentation.objects.all('-deadline')
    serializer_class = PresentationSerializer


class PresentationUpdateView(UpdateAPIView):
    queryset = Subject.objects.all()
    serializer_class = PresentationSerializer
    lookup_field = "pk"
    permission_classes = [IsAuthenticated, IsAdmin, IsAlive]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.subject = request.data.get("subject")
        instance.save()

        return Response({"msg": "presentation updated"}, status=status.HTTP_200_OK)

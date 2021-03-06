from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Count
import mimetypes
import datetime
from apiv1.permissions import IsAdmin, IsAlive
from shive_back import settings
from .serializers import *
from rest_framework import parsers, renderers
from rest_framework.authtoken.models import Token
from rest_framework.compat import coreapi, coreschema
from rest_framework.schemas import ManualSchema
from rest_framework.views import APIView
import pprint

from .models import Profile, User, Semester, Subject, Team, Presentation, Comment, AssignmentSubject, Assignment


# Create your views here.


class ProfileCreateView(CreateAPIView):
    serializer_class = SignupSerializer

    def post(self, request, *args, **kwargs):
        try:
            u = User.objects.get(username=request.data.get('student_no'))
            p = Profile.objects.get(user=u)

            return Response({"msg": "user already exists"}, status=status.HTTP_409_CONFLICT)

        except User.DoesNotExist or Profile.DoesNotExist:
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
    queryset = Profile.objects.filter(team=None, is_deleted=False, is_admin=False)


class TeamListView(ListAPIView):
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated, IsAlive]
    queryset = Team.objects.all()


class TeamCreateView(CreateAPIView):
    serializer_class = ProfileSerializer(many=True)
    permission_classes = [IsAuthenticated, IsAlive, IsAdmin]

    def post(self, request, *args, **kwargs):
        pres = Presentation()
        team = Team()
        pres.save()
        # team.save()
        team.presentation = pres
        pres.save()
        team.save()

        # atp = Presentation.objects.filter(team=team)
        # if atp:
        #     p = atp.first()
        # else:
        # pres = Presentation.objects.create()
        # team.presentation = pres
        # team.save()
        # pres.save()

        if self.request.data.get("subject"):
            pres.subject = Subject.objects.get(pk=self.request.data.get("subject"))
            pres.save()

        if self.request.data.get("deadline"):
            pres.deadline = self.request.data.get("deadline")
            pres.save()

        for pk in self.request.data.get("profiles"):
            pro = Profile.objects.get(pk=pk)
            pro.team = team
            pro.save()

        return Response({"msg": "team created"}, status=status.HTTP_201_CREATED)


class TeamDeleteView(DestroyAPIView):
    lookup_field = "pk"
    permission_classes = [IsAuthenticated, IsAdmin, IsAlive]
    queryset = Team.objects.all()

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.presentation.delete()
        instance.delete()

        return Response({"msg": "team deleted"}, status=status.HTTP_200_OK)


class TeamRetrieveView(RetrieveAPIView):
    serializer_class = TeamSerializer
    queryset = Team.objects.all()
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'


class TeamEditCreateView(CreateAPIView):
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated, IsAdmin, IsAlive]

    # profiles - subject - deadline
    def post(self, request, *args, **kwargs):
        t = Team.objects.get(pk=self.kwargs.get("pk"))

        a = t.profiles.all()
        b = self.request.data.get("profiles")

        if t.presentation:
            p = t.presentation
        else:
            p = Presentation.objects.create()
            t.presentation = p
            t.save()

        if self.request.data.get("subject"):
            p.subject = p.subject = Subject.objects.get(pk=self.request.data.get("subject"))
            p.save()

        if self.request.data.get("deadline"):
            p.deadline = self.request.data.get("deadline")
            p.save()

        for i in b:
            u = Profile.objects.get(pk=i)
            if u not in a:
                u.team = t
                u.save()

        for i in a:
            if i.pk not in b:
                i.team = None
                i.save()

        return Response({"msg": "team edited"}, status=status.HTTP_200_OK)


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
            u = p.user
            p.delete()
            u.delete()

        return Response({"msg": "profiles deleted"}, status=status.HTTP_200_OK)


class PresentationCreateView(CreateAPIView):
    permission_classes = [IsAdmin, IsAlive, IsAuthenticated]
    serializer_class = SubjectSerializer

    def post(self, request, *args, **kwargs):
        t = Team.objects.get(pk=self.request.data.get("team"))
        s = Subject.objects.get(pk=self.request.data.get("subject"))

        if t.presentation:
            t.presentation.subject = s
            t.save()

        else:
            p = Presentation.objects.create(subject=s)
            t.presentation = p
            t.save()

        try:
            t.presentation.deadline = self.request.data.get("deadline")
            t.presentation.save()
        except:
            pass

        return Response({"msg": "presentation created"}, status=status.HTTP_201_CREATED)


class PresentationListView(ListAPIView):
    permission_classes = []
    queryset = Presentation.objects.all().order_by('-deadline')
    serializer_class = PresentationSerializer


class PresentationUpdateView(UpdateAPIView):
    queryset = Presentation.objects.all()
    serializer_class = PresentationSerializer
    lookup_field = "pk"
    permission_classes = [IsAuthenticated, IsAlive]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # instance.subject = request.data.get("subject")
        instance.description = request.data.get("description")
        instance.save()

        return Response({"msg": "presentation updated"}, status=status.HTTP_200_OK)


class PresentationDeleteView(DestroyAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    lookup_field = "pk"
    permission_classes = [IsAuthenticated, IsAdmin, IsAlive]

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.presentation.subject = None
        instance.presentation.save()
        instance.save()

        return Response({"msg": "subject removed from presentation"}, status=status.HTTP_200_OK)


class CommentCreateView(CreateAPIView):
    serializer_class = CommentSerializer
    lookup_field = "pk"
    queryset = Presentation.objects.all()
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        p = Profile.objects.get(user=self.request.user)
        Comment.objects.create(presentation=instance, profile=p, text=self.request.data.get("text"))

        return Response({"msg": "comment created"}, status=status.HTTP_201_CREATED)


class CommentListView(ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        p = Presentation.objects.get(pk=self.kwargs.get("pk"))
        return p.comments.all()


class MyObtainAuthToken(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = MyAuthTokenSerializer
    if coreapi is not None and coreschema is not None:
        schema = ManualSchema(
            fields=[
                coreapi.Field(
                    name="username",
                    required=True,
                    location='form',
                    schema=coreschema.String(
                        title="Username",
                        description="Valid username for authentication",
                    ),
                ),
                coreapi.Field(
                    name="password",
                    required=True,
                    location='form',
                    schema=coreschema.String(
                        title="Password",
                        description="Valid password for authentication",
                    ),
                ),
            ],
            encoding="application/json",
        )

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        p = Profile.objects.get(user=user)
        if p.is_deleted:
            return Response({"msg": "profile is not accepted yet"}, status=status.HTTP_401_UNAUTHORIZED)
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})


class RoleApiView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = Profile

    def get(self, request, *args, **kwargs):
        p = Profile.objects.get(user=self.request.user)

        if p.is_admin:
            return Response({"role": "admin"}, status=status.HTTP_200_OK)

        elif p.is_deleted:
            return Response({"role": "not accepted"}, status=status.HTTP_200_OK)

        else:
            return Response({"role": "accepted"}, status=status.HTTP_200_OK)


class CurrentPresentationGetView(ListAPIView):
    serializer_class = CurrentPresentationSerializer

    # permission_classes =

    def get_queryset(self):
        today = datetime.date.today()
        print("today: ", today)
        all_pres = Presentation.objects.filter(deadline__gte=today).order_by('deadline')
        print(all_pres)

        if all_pres:
            return all_pres[:1]
        else:
            return None


class ArchiveListView(ListAPIView):
    serializer_class = CurrentPresentationSerializer

    def get_queryset(self):
        today = datetime.date.today()
        # print("today: ", today)
        all_pres = Presentation.objects.filter(deadline__lt=today).order_by('-deadline')
        # print(all_pres)

        return all_pres


class RatingCreateView(CreateAPIView):
    serializer_class = PresentationSerializer
    permission_classes = [IsAuthenticated, IsAlive]
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'
    queryset = Presentation.objects.all()

    def post(self, request, *args, **kwargs):
        pres = self.get_object()
        p = Profile.objects.get(user=self.request.user)

        try:
            ra = Rating.objects.get(presentation=pres, profile=p)
        except Rating.DoesNotExist:
            ra = Rating.objects.create(presentation=pres, profile=p)

        ra.rating = int(self.request.data.get("rating"))
        ra.save()

        return Response({"msg": "ok"}, status=status.HTTP_200_OK)


class ProfileTeamPresentationView(ListAPIView):
    serializer_class = PresentationSerializer
    permission_classes = [IsAuthenticated, IsAlive]

    def get_queryset(self):
        p = Profile.objects.get(user=self.request.user)
        if not p.team:
            return None
        return [p.team.presentation]


class FileCreateView(CreateAPIView):
    serializer_class = PresentationSerializer
    permission_classes = [IsAuthenticated, IsAlive]
    lookup_url_kwarg = 'pk'
    lookup_field = 'pk'

    def post(self, request, *args, **kwargs):
        pass


class FileUploadView(APIView):
    parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated, IsAlive]

    def post(self, request, pk, format=None):
        # print("bzo boz e qandi")
        fil = request.data.get("file")
        # print(request.FILES['file'])
        # fil = request.FILES['file']
        # # do some stuff with uploaded file
        a = File.objects.create(profile=Profile.objects.get(user=self.request.user), file=fil,
                                name=self.request.data.get("name"), link=" sfg",
                                presentation=Presentation.objects.get(pk=self.kwargs.get("pk")))
        a.link = "https://cdn.atelier-team.ir/shive/" + a.file.name
        a.size = a.file.size
        a.save()

        return Response({"msg": "file created"}, status=status.HTTP_200_OK)


class SemesterListView(ListAPIView):
    serializer_class = SemesterSerializer
    queryset = Semester.objects.all().order_by('-pk')


class PresentationBySemesterListView(ListAPIView):
    serializer_class = CurrentPresentationSerializer

    # queryset = Semester.objects.all()

    def get_queryset(self):
        ss = Semester.objects.get(pk=self.kwargs.get('pk'))
        today = datetime.date.today()
        # print("today: ", today)
        all_pres = Presentation.objects.filter(deadline__lt=today, subject__semester=ss).order_by('-deadline')
        return all_pres


class AnnouncementCreateView(CreateAPIView):
    serializer_class = AnnouncementSerializer
    permission_classes = [IsAlive, IsAuthenticated, IsAdmin]

    def create(self, request, *args, **kwargs):
        a = Announcement.objects.create(title=self.request.data.get("title"),
                                        description=self.request.data.get("description"))

        return Response({"msg": "ann created", "pk": a.pk}, status=status.HTTP_201_CREATED)


class AnnFileUploadView(APIView):
    parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated, IsAlive]

    def post(self, request, pk, format=None):
        # print("bzo boz e qandi")
        fil = request.data.get("file")
        # print(request.FILES['file'])
        # fil = request.FILES['file']
        # # do some stuff with uploaded file
        AnnouncementFile.objects.create(file=fil, title=self.request.data.get("title"),
                                        announcement=Announcement.objects.get(pk=self.kwargs.get("pk")))

        return Response({"msg": "file created"}, status=status.HTTP_200_OK)


class FileDeleteView(DestroyAPIView):
    serializer_class = FileSerializer
    queryset = File.objects.all()
    lookup_url_kwarg = 'pk'
    lookup_field = 'pk'

    def delete(self, request, *args, **kwargs):
        f = self.get_object()
        f.delete()
        return Response({"msg": "deleted"}, status=status.HTTP_200_OK)


class AnnListVIew(ListAPIView):
    serializer_class = AnnouncementSerializer
    queryset = Announcement.objects.all().order_by('-pk')


class VideoCommentCreateView(CreateAPIView):
    serializer_class = VideoCommentSerializer
    permission_classes = [IsAuthenticated, IsAlive]
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'
    queryset = File.objects.all()

    def post(self, request, *args, **kwargs):
        fil = self.get_object()
        # serializer = VideoCommentSerializer(data=)
        VideoComment.objects.create(video=fil, profile=Profile.objects.get(user=self.request.user),
                                    time=self.request.data.get("time"), text=self.request.data.get("text"))

        return Response({"msg": "created"}, status=status.HTTP_201_CREATED)


class VideoCommentListView(ListAPIView):
    serializer_class = VideoCommentSerializer
    permission_classes = []

    def get_queryset(self):
        fil = File.objects.get(pk=self.kwargs.get("pk"))

        return fil.comments.all()


class VideoDownloadView(ListAPIView):
    # permission_classes =
    serializer_class = FileSerializer

    # lookup_url_kwarg = 'pk'
    # lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        f = File.objects.get(pk=self.kwargs.get('pk'))

        response = HttpResponse(content_type='mimetype', status=status.HTTP_206_PARTIAL_CONTENT)
        response['Content-Disposition'] = "attachment; filename=%s" % f.file.name
        response['Accept-Ranges'] = 'bytes'
        response['X-Accel-Redirect'] = settings.MEDIA_URL + '/' + f.file.name
        response['X-Accel-Buffering'] = 'yes'
        return response


class AssignmentSubjectListView(ListAPIView):
    serializer_class = AssignmentSubjectSerializer
    queryset = AssignmentSubject.objects.all()


class AssignmentListView(ListAPIView):
    serializer_class = AssignmentSerializer

    def get_queryset(self):
        p = self.kwargs.get('pk')
        return Assignment.objects.filter(subject=p)


class AssignmentCreateView(CreateAPIView):
    serializer_class = AssignmentSerializer
    permission_classes = [IsAlive, IsAuthenticated]

    def create(self, request, *args, **kwargs):
        p = self.request.user
        p = Profile.objects.get(user=p)
        a = Assignment.objects.create(name=self.request.data.get("name"), profile=p,
                                      subject=AssignmentSubject.objects.get(pk=self.request.data.get("subjectId")))

        return Response({"msg": "assignment created", "pk": a.pk}, status=status.HTTP_201_CREATED)


class AssignmentFileUploadView(APIView):
    parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated, IsAlive]

    def post(self, request, pk, format=None):
        fil = request.data.get("file")

        a = AssignmentFile.objects.create(file=fil, title=self.request.data.get("title"),
                                          assignment=Assignment.objects.get(pk=self.kwargs.get("pk")))
        a.size = a.file.size
        a.save()
        return Response({"msg": "file created"}, status=status.HTTP_200_OK)


class IssueListView(ListAPIView):
    serializer_class = IssueSerializer
    permission_classes = [IsAlive, IsAdmin]
    queryset = Issue.objects.filter(status='waiting')


class IssueCreateView(CreateAPIView):
    serializer_class = IssueSerializer
    permission_classes = [IsAlive, IsAuthenticated]

    def create(self, request, *args, **kwargs):
        p = self.request.user
        p = Profile.objects.get(user=p)
        a = Issue.objects.create(profile=p, title=self.request.data.get("title"),
                                 description=self.request.data.get("description"))

        return Response({"msg": "issue created", "pk": a.pk}, status=status.HTTP_201_CREATED)


class IssueFileUploadView(APIView):
    parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated, IsAlive]

    def post(self, request, pk, format=None):
        fil = request.data.get("file")

        a = IssueFile.objects.create(file=fil, title=self.request.data.get("title"),
                                     issue=Issue.objects.get(pk=self.kwargs.get("pk")))
        # a.size = a.file.size
        # a.save()
        return Response({"msg": "file created"}, status=status.HTTP_200_OK)

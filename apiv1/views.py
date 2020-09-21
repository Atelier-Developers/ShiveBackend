from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apiv1.permissions import IsAdmin, IsAlive
from .serializers import SignupSerializer, SubjectSerializer

from .models import Profile, User, Semester


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


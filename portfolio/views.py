from django.contrib.auth import logout, login
from django.contrib.auth.models import Group
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from portfolio.models import User, Role, Feedback, Contact, Project, Portfolio, ProjectContributor, Files, ProjectUser
from portfolio.permissions import IsModerator, IsAuthenticatedForDetailOrReadOnly, \
    FileProjectContributorPermission, FeedbackContactPermission, SuperAdminPermission
from portfolio.serializers import LoginSerializer, UserSerializer, RegisterSerializer, FeedbackSerializer, \
    ContactSerializer, ProjectSerializer, PortfolioSerializer, ProjectContributerSerializer, FilesSerializer, \
    ProjectUserSerializer, ModeratorSerializer
from . import permissions
from .paginations import CustomPagination


class HelloAPIView(APIView):
    def get(self, request):
        return Response(data={"Message": "HelloWorld"})


class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get("user")
        login(request, user)
        return Response(UserSerializer(user).data)


class RegisterAPIView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(data={"message": "User created successfully"})


class LogoutAPIView(APIView):
    def post(self, request):
        logout(request)
        return Response(data={"message": "User logout"})


class SessionAPIView(APIView):
    def get(self, request):
        if request.user.is_anonymous:
            return Response(data={"message": "User should login"})
        return Response(UserSerializer(request.user).data)



class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsModerator | permissions.IsAuthenticatedForDetailOrReadOnly]  # Moderators CRUD, Users can only GET
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['title']
    search_fields = ['title', 'description']


class PortfolioViewSet(viewsets.ModelViewSet):
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer
    permission_classes = [IsModerator | permissions.IsAuthenticatedForDetailOrReadOnly]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['title']
    search_fields = ['title', 'description']


class ProjectContributerViewSet(viewsets.ModelViewSet):
    queryset = ProjectContributor.objects.all()
    serializer_class = ProjectContributerSerializer
    permission_classes = [IsModerator | FileProjectContributorPermission]  # CRUD for Moderators, GET for Authenticated Users
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['position', 'github_link', 'linkedin_link']
    search_fields = ['full_name', 'position']


class FilesViewSet(viewsets.ModelViewSet):
    queryset = Files.objects.all()
    serializer_class = FilesSerializer
    permission_classes = [IsModerator | FileProjectContributorPermission]  # CRUD for Moderators, GET for Authenticated Users
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['project']
    search_fields = ['title', 'description']

class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [FeedbackContactPermission]


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [FeedbackContactPermission]

class ModeratorViewSet(viewsets.ModelViewSet):
    serializer_class = ModeratorSerializer
    permission_classes = [SuperAdminPermission]

    def get_queryset(self):
        return User.objects.filter(role__name="Moderator")  # List only Moderators

    def perform_create(self, serializer):
        moderator_role, _ = Role.objects.get_or_create(name="Moderator")
        serializer.save(role=moderator_role)

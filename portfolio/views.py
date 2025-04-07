from django.contrib.auth import authenticate
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, generics, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Project, Portfolio, ProjectContributor, Files, Feedback, Contact, User, Role, ProjectUser, Category, \
    CategoryProject
from .permissions import (
    IsModeratorOrSuperAdmin,
    SuperAdminOnly,
    IsModeratorOrReadOnly,
    ReadOnlyOrAuthenticatedForSpecialModels,
    IsOwnerOrReadOnlyForContacts,
    FeedbackPermission
)
from .serializers import (
    ProjectSerializer, PortfolioSerializer, ProjectContributerSerializer,
    FilesSerializer, FeedbackSerializer, ContactSerializer, ModeratorSerializer, CustomTokenObtainPairSerializer,
    UserRegistrationSerializer, LoginSerializer, UserSerializer, ProjectUserSerializer, CategorySerializer,
    CategoryProjectSerializer
)
from .paginations import CustomPagination


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class HelloAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response(data={"message": "Hello World"})


class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Register a new user",
        responses={
            201: "User created successfully",
            400: "Bad Request - Invalid data"
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {"message": "User created successfully"},
            status=status.HTTP_201_CREATED
        )

    def perform_create(self, serializer):
        serializer.save()


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            user = authenticate(email=email, password=password)
            if user:
                refresh = RefreshToken.for_user(user)
                return Response(
                    {
                        "access_token": str(refresh.access_token),
                        "refresh_token": str(refresh)
                    }, status=status.HTTP_200_OK
                )
            return Response({"error": "Email or Password incorrect"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Successfully logged out"})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class SessionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [ReadOnlyOrAuthenticatedForSpecialModels]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['title']
    search_fields = ['title', 'description']


class PortfolioViewSet(viewsets.ModelViewSet):
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer
    permission_classes = [ReadOnlyOrAuthenticatedForSpecialModels]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['title']
    search_fields = ['title', 'description']


class ProjectContributerViewSet(viewsets.ModelViewSet):
    queryset = ProjectContributor.objects.all()
    serializer_class = ProjectContributerSerializer
    permission_classes = [ReadOnlyOrAuthenticatedForSpecialModels]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['position', 'github_link', 'linkedin_link']
    search_fields = ['full_name', 'position']


class FilesViewSet(viewsets.ModelViewSet):
    queryset = Files.objects.all()
    serializer_class = FilesSerializer
    permission_classes = [IsAuthenticated]  # Files require authentication
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['project']
    search_fields = ['title', 'description']


class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [FeedbackPermission]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['project']
    search_fields = ['message']


class ContactViewSet(viewsets.ModelViewSet):
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnlyForContacts]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['name', 'email', 'message']

    def get_queryset(self):
        return Contact.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ModeratorViewSet(viewsets.ModelViewSet):
    serializer_class = ModeratorSerializer
    permission_classes = [SuperAdminOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['email', 'first_name', 'last_name']

    def get_queryset(self):
        return User.objects.filter(role__name="Moderator")

    def perform_create(self, serializer):
        moderator_role, _ = Role.objects.get_or_create(name="Moderator")
        serializer.save(role=moderator_role)


class ProjectUserViewSet(viewsets.ModelViewSet):
    queryset = ProjectUser.objects.all()
    serializer_class = ProjectUserSerializer
    permission_classes = [ReadOnlyOrAuthenticatedForSpecialModels]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['project', 'contributor']
    search_fields = ['project__title', 'contributor__full_name']


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [ReadOnlyOrAuthenticatedForSpecialModels]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['name']
    search_fields = ['name']


class CategoryProjectViewSet(viewsets.ModelViewSet):
    queryset = CategoryProject.objects.all()
    serializer_class = CategoryProjectSerializer
    permission_classes = [ReadOnlyOrAuthenticatedForSpecialModels]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['project', 'category']
    search_fields = ['project__title', 'category__name']
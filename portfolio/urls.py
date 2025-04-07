from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from portfolio.models import Category
from portfolio.views import (
    ProjectViewSet, PortfolioViewSet, ProjectContributerViewSet, FilesViewSet,
    FeedbackViewSet, ContactViewSet, ModeratorViewSet, LoginView, RegisterView,
    LogoutAPIView, SessionAPIView, HelloAPIView, CustomTokenObtainPairView, CategoryViewSet, CategoryProjectViewSet,
    ProjectUserViewSet
)

router = DefaultRouter()

# Registering ViewSets
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'portfolios', PortfolioViewSet, basename='portfolio')
router.register(r'project-contributors', ProjectContributerViewSet, basename='project-contributor')
router.register(r'files', FilesViewSet, basename='file')
router.register(r'feedback', FeedbackViewSet, basename='feedback')
router.register(r'contacts', ContactViewSet, basename='contact')
router.register(r'moderators', ModeratorViewSet, basename='moderator')
router.register(r'category', CategoryViewSet, basename='category')
router.register(r'category_project', CategoryProjectViewSet, basename='category_project')
router.register(r'project_user', ProjectUserViewSet, basename='project_user')

urlpatterns = [
    path('', include(router.urls)),  # API ViewSets
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('session/', SessionAPIView.as_view(), name='session'),
    path('', HelloAPIView.as_view(), name='hello'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]

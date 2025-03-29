from django.urls import path, include
from rest_framework.routers import DefaultRouter
from portfolio.views import (
    ProjectViewSet, PortfolioViewSet, ProjectContributerViewSet, FilesViewSet,
    FeedbackViewSet, ContactViewSet, ModeratorViewSet, LoginAPIView, RegisterAPIView,
    LogoutAPIView, SessionAPIView, HelloAPIView
)

router = DefaultRouter()

# Registering ViewSets
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'portfolios', PortfolioViewSet, basename='portfolio')
router.register(r'project-contributors', ProjectContributerViewSet, basename='project-contributor')
router.register(r'files', FilesViewSet, basename='file')
router.register(r'feedback', FeedbackViewSet, basename='feedback')
router.register(r'contacts', ContactViewSet, basename='contact')
router.register(r'moderators', ModeratorViewSet, basename='moderator')  # SuperAdmin can create Moderators

urlpatterns = [
    path('', include(router.urls)),  # API ViewSets
    path('login/', LoginAPIView.as_view(), name='login'),
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('session/', SessionAPIView.as_view(), name='session'),
    path('', HelloAPIView.as_view(), name='hello')
]
from rest_framework import permissions


class IsModerator(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and getattr(request.user, 'role',
                                                                          None) and request.user.role.name == "Moderator"


class IsAuthenticatedForDetailOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action == 'retrieve':
            return request.user.is_authenticated
        return True


class FeedbackContactPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        if request.method == 'POST':
            return not getattr(request.user, 'role', None) or request.user.role.name != "Moderator"
        return False


class FileProjectContributorPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        return False


class SuperAdminPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        return request.user.role.name == "SuperAdmin" and request.method in ["POST", "GET"]

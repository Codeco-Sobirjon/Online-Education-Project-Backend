from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuth(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.groups.filter(name='admin').exists()
    

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS or request.user.is_authenticated and
                request.user.groups.filter(name='admin').exists())


class IsAdminOrAuth(BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated and
                (request.method in SAFE_METHODS or request.user.groups.filter(name='admin').exists()))


class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.groups.filter(name='teacher').exists()


class IsAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

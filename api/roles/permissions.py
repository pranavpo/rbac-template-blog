from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'admin'

class IsEditor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'editor'

class IsWriter(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'writer'

class CanEditBlog(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Admins and Editors can edit blogs
        if request.user.role in ['admin', 'editor']:
            return True
        return False

class CanWriteBlog(permissions.BasePermission):
    def has_permission(self, request, view):
        # Only Admins and Writers can create blogs
        if request.user.is_authenticated and request.user.role in ['admin', 'writer']:
            return True
        return False


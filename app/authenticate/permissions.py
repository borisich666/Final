from rest_framework import permissions


class IsCompanyOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'company'):
            return request.user == obj.company.owner
        return False


class IsCompanyEmployee(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.company is not None
from rest_framework.permissions import BasePermission, SAFE_METHODS


class CreatePermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return request.user.is_staff
        return False

from rest_framework.permissions import BasePermission

from apiv1.models import Profile


class IsAdmin(BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        p = Profile.objects.get(user=request.user)
        return p.is_admin


class IsAlive(BasePermission):
    """
    Allows access only to not deleted users.
    """

    def has_permission(self, request, view):
        p = Profile.objects.get(user=request.user)
        return not p.is_deleted

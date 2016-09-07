from rest_framework import permissions

class OnlyOwnerAllowedAny(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if obj.owner != None:
            return obj.owner == request.user

        return True

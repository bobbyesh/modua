from rest_framework import permissions

class OnlyOwnerAllowedAny(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if obj.user != None:
            return obj.user == request.user

        return True

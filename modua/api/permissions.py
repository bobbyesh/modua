from rest_framework import permissions

class OnlyOwnerCanAccess(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if obj.owner != None:
            return obj.owner == request.user

        return True

class OnlyOwnerCanDelete(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method == 'DELETE':
            return obj.owner == request.user
        else:
            return True


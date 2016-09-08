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

class NoPutAllowed(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.method != 'PUT'


class OnlyEaseCanChange(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method == 'PATCH' or request.method == 'PUT':
            for elem in request.data.keys():
                if elem != 'ease':
                    return False
        return True

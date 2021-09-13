from rest_framework.permissions import BasePermission


class IsStaffOrIsAdmin(BasePermission):
    # create, listing
    # def has_permission(self, request, view):

    # update, partial_update, destroy, retrieve
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff, not request.user.is_student


class IsStudent(BasePermission):
    # create, listing
    # def has_permission(self, request, view):

    # update, partial_update, destroy, retrieve
    def has_object_permission(self, request, view, obj):
        return request.user.is_student

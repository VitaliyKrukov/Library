from rest_framework import permissions


class IsIssuanceOwnerOrAdmin(permissions.BasePermission):
    """
    Разрешение, позволяющее пользователям работать только со своими выдачами.
    Администраторы имеют доступ ко всем выдачам.
    """

    def has_object_permission(self, request, view, obj):
        # Администраторам разрешено все
        if request.user and request.user.is_staff:
            return True

        # Пользователи могут работать только со своими выдачами
        return obj.user == request.user

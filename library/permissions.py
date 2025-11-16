from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Разрешение на изменение только для администраторов.
    Остальные могут только просматривать.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class IsIssuanceOwnerOrAdmin(permissions.BasePermission):
    """
    Разрешение, позволяющее пользователям работать только со своими выдачами.
    Администраторы имеют доступ ко всем выдачам.
    """

    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_staff:
            return True
        return obj.user == request.user

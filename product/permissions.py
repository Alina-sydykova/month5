


from rest_framework import permissions

class IsModerator(permissions.BasePermission):
    """
    Кастомный permission для модераторов:
    
    1. Модератор должен быть is_staff=True.
    2. Может просматривать, изменять и удалять чужие продукты.
    3. Не может создавать продукты (POST запрещён).
    """

    def has_permission(self, request, view):
        if request.method == 'POST':
            return False

        return request.user and request.user.is_staff

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS or request.method in ['PUT', 'PATCH', 'DELETE']:
            return request.user and request.user.is_staff

        
        return False

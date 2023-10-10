from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsCreatorOrReadOnly(BasePermission):
    """Custom permissions for creator"""
    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        if request.method in SAFE_METHODS:
            return True
        
        return obj.creator == request.user
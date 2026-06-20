from rest_framework import permissions


class AdminOrReadOnly(permissions.IsAdminUser):
    
    def has_permission(self, request, view):
        admin_permission = bool(request.user and request.user.is_staff)
        return request.method == 'GET' or admin_permission
    
    
    
    #slightly Updated or Improved modern version for same custom permission:
    #SAEF_METHODS means a built in tuple with GET,HEAD, OPTIONS. The above permission function can blocked the HEAD and OPTION method.
    
    '''
    
    def has_permission(self, request, view):

        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user and request.user.is_staff
        
    '''
    

class ReviewUserOrReadOnly(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        else:
            return obj.reviewer == request.user
        
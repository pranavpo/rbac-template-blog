from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Blog
from .serializers import BlogSerializer
from .permissions import IsAdmin, IsEditor, IsWriter, CanEditBlog, CanWriteBlog

class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

    def get_permissions(self):
        """ Set different permissions for different actions. """
        if self.action in ['list', 'retrieve']:  # ✅ Everyone can view blogs
            permission_classes = [AllowAny]
        elif self.action == "create":  # ✅ Admins & Writers can create blogs
            permission_classes = [IsAuthenticated, CanWriteBlog]
        elif self.action in ['update', 'partial_update']:  # ✅ Admins & Editors can edit blogs
            permission_classes = [IsAuthenticated, CanEditBlog]
        elif self.action == 'destroy':  # ✅ Only Admins can delete blogs
            permission_classes = [IsAuthenticated, IsAdmin]
        else:
            permission_classes = [IsAuthenticated]  # ✅ Default for other cases

        return [permission() for permission in permission_classes]

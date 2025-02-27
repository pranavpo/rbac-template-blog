from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Blog
from .serializers import BlogSerializer
from .permissions import IsAdmin, IsEditor, IsWriter, CanEditBlog, CanWriteBlog
from rest_framework.decorators import api_view, action
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status

class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

    def get_permissions(self):
        """ Set different permissions for different actions. """
        if self.action in ['list', 'retrieve']:  # ✅ Everyone can view blogs
            permission_classes = [AllowAny]
        elif self.action == "create":  # ✅ Writers & Admins can create blogs
            permission_classes = [IsAuthenticated, IsWriter]
        elif self.action in ['update', 'partial_update']:  # ✅ Editors & Admins can edit blogs
            permission_classes = [IsAuthenticated, CanEditBlog]
        elif self.action == 'destroy':  # ✅ Only Admins can delete blogs
            permission_classes = [IsAuthenticated, IsAdmin]
        else:
            permission_classes = [IsAuthenticated]  # ✅ Default for other cases

        return [permission() for permission in permission_classes]

    @action(detail=True, methods=['patch'], permission_classes=[IsAuthenticated])
    def update_status(self, request, pk=None):
        """ Custom action to update only the blog status with role-based restrictions """
        blog = self.get_object()
        new_status = request.data.get("status")

        if new_status not in ['draft', 'pending_review', 'published']:
            return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)

        # Restrict Writers: Can only move draft → pending_review
        if request.user.role == "writer":
            if blog.status == "draft" and new_status == "pending_review":
                blog.status = "pending_review"
                blog.save()
                return Response({"message": "Blog submitted for review", "status": blog.status}, status=status.HTTP_200_OK)
            return Response({"error": "Writers can only move draft → pending_review"}, status=status.HTTP_403_FORBIDDEN)

        # Editors: Can move pending_review → published
        if request.user.role == "editor":
            if blog.status == "pending_review" and new_status == "published":
                blog.status = "published"
                blog.save()
                return Response({"message": "Blog has been published", "status": blog.status}, status=status.HTTP_200_OK)
            return Response({"error": "Editors can only move pending_review → published"}, status=status.HTTP_403_FORBIDDEN)

        # Admins: Full control
        if request.user.role == "admin":
            blog.status = new_status
            blog.save()
            return Response({"message": f"Blog status changed to {new_status}", "status": blog.status}, status=status.HTTP_200_OK)

        return Response({"error": "Unauthorized action"}, status=status.HTTP_403_FORBIDDEN)



@api_view(['POST'])
def login_user(request):
    """Authenticate user and return Token"""
    username = request.data.get("username")
    password = request.data.get("password")

    user = User.objects.filter(username=username).first()
    if user and user.check_password(password):
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=status.HTTP_200_OK)
    return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
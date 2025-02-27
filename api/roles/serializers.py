from rest_framework import serializers
from .models import Blog

class BlogSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')  # Ensures author is not changed manually

    class Meta:
        model = Blog
        fields = ['id', 'title', 'content', 'status', 'author', 'created_at', 'updated_at']
        read_only_fields = ['id', 'author', 'created_at']

    def create(self, validated_data):
        """ Set the author to the logged-in user when creating a blog post. """
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)

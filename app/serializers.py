from rest_framework import serializers
from app.models import Image


class ImageSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='image_id', read_only=True)
    classes = serializers.ListField(source='class_numbers')
    class Meta:
        model = Image
        fields = ('id', 'description', 'classes')

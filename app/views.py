from django.db.models import Count

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

from app.models import Image
from .serializers import ImageSerializer

# Create your views here.


class GetClasses(APIView):
    renderer_classes = (JSONRenderer, )

    def get_queryset(self, required_classes, forbidden_classes):
        return Image.objects.exclude(
            # First exclude images related to forbidden classes.
            classes__class_number__in=forbidden_classes
        ).filter(
            # Then count required classes for each image remaining.
            classes__class_number__in=required_classes
        ).annotate(
            required_classes_count=Count('classes__class_number')
        ).filter(
            # If count matches, all required classes are present.
            required_classes_count=len(required_classes)
        ).prefetch_related('classes')

    def get(self, request, required_classes, forbidden_classes):
        serializer = ImageSerializer(self.get_queryset(required_classes, forbidden_classes), many=True)
        return Response({'result': serializer.data})

from django.db.models import Count

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

from app.models import Image
from .serializers import ImageSerializer

# Create your views here.


class GetClasses(APIView):
    renderer_classes = (JSONRenderer, )

    def get(self, request, required_classes, forbidden_classes):
        queryset = Image.objects\
            .exclude(classes__class_number__in=forbidden_classes)\
            .filter(classes__class_number__in=required_classes)\
            .annotate(required_classes_count=Count('classes__class_number'))\
            .filter(required_classes_count=len(required_classes))\
            .prefetch_related('classes')

        serializer = ImageSerializer(queryset.all(), many=True)
        return Response({'result': serializer.data})

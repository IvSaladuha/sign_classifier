from collections import OrderedDict
from django.test import TestCase

# Create your tests here.
from app.models import Image, ImageClass
from app.serializers import ImageSerializer
from app.views import GetClasses


class ImageTestCase(TestCase):
    def setUp(self):
        Image.objects.create(id=1, image_id="12345", description="The Image")
        ImageClass.objects.create(id=1, image_id=1, class_number=3)
        ImageClass.objects.create(id=2, image_id=1, class_number=4)

    def test_image_class_numbers(self):
        """Testing Image.class_numbers property."""
        img = Image.objects.get(id=1)
        self.assertEqual(list(img.class_numbers), [3, 4])

    def test_serializer(self):
        serializer = ImageSerializer(Image.objects.filter(id=1), many=True)
        self.assertEqual(serializer.data, [
            OrderedDict([("id", 12345), ("description", "The Image"), ("classes", [3, 4])])
        ])

    def tearDown(self):
        Image.objects.all().delete()


class GetClassesTestCase(TestCase):
    def setUp(self):
        Image.objects.create(id=1, image_id="12345", description="The Image")
        Image.objects.create(id=2, image_id="23456", description="The Second Image")
        Image.objects.create(id=3, image_id="34567", description="The Third Image")
        ImageClass.objects.create(id=1, image_id=1, class_number=3)
        ImageClass.objects.create(id=2, image_id=1, class_number=4)
        ImageClass.objects.create(id=3, image_id=2, class_number=4)
        ImageClass.objects.create(id=4, image_id=2, class_number=5)
        ImageClass.objects.create(id=5, image_id=3, class_number=3)
        ImageClass.objects.create(id=6, image_id=3, class_number=4)
        ImageClass.objects.create(id=7, image_id=3, class_number=5)

    def test_queryset(self):
        v = GetClasses()

        result = v.get_queryset([], [5])
        self.assertEqual(len(result), 0)

        result = v.get_queryset([3], [5])
        self.assertEqual(len(result), 1)
        self.assertEqual(result.get().id, 1)

        result = v.get_queryset([3], [4, 5])
        self.assertEqual(len(result), 0)

        result = v.get_queryset([3, 4], [5])
        self.assertEqual(len(result), 1)
        self.assertEqual(result.get().id, 1)

        result = v.get_queryset([4, 5], [3])
        self.assertEqual(len(result), 1)
        self.assertEqual(result.get().id, 2)

        result = v.get_queryset([4, 5], [])
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].id, 2)
        self.assertEqual(result[1].id, 3)

    def tearDown(self):
        Image.objects.all().delete()

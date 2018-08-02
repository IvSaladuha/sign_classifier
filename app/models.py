from django.db import models

# Create your models here.


class Image(models.Model):
    """Image record."""
    image_id = models.CharField(max_length=50)
    description = models.CharField(max_length=1000)

    @property
    def class_numbers(self):
        return self.classes.values_list('class_number', flat=True).all()


class ImageClass(models.Model):
    image = models.ForeignKey(Image, related_name='classes', on_delete=models.CASCADE)
    class_number = models.IntegerField()

    class Meta:
        indexes = [
            models.Index(fields=['class_number'])
        ]
        unique_together = (('image', 'class_number'),)

from django.db import models
import uuid
from api.category.models import Category
import sys
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files import File

# Create your models here.
TYPE = (
    ("V", "Veg"),
    ("NV", "Non-Veg"),
)


def compress(image):
    im = Image.open(image)
    im_io = BytesIO()
    im.save(im_io, "JPEG", quality=60)
    ext = image.name.split(".")[-1]
    image_name = str(uuid.uuid4()) + "." + ext
    print("#####################################> ", image_name)
    new_image = File(im_io, name=image_name)
    return new_image


class Menu(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    image = models.ImageField(upload_to="images/", blank=True, null=True)
    type = models.CharField(("Dish type"), choices=TYPE, max_length=3)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        new_image = compress(self.image)
        self.image = new_image
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Menu"
        verbose_name_plural = "Menus"

from django.db import models

CLOTH = "C"
SPORT_TOOL = "S"


class Size(models.Model):
    size = models.CharField(max_length=50)

    def __str__(self):
        return self.size


class Color(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class Product(models.Model):
    TYPES = (
        (CLOTH, "Cloth"),
        (SPORT_TOOL, "Sport tool"),
    )

    title = models.CharField(max_length=100)
    price = models.FloatField()
    amount = models.IntegerField()
    rating = models.FloatField(default=0)
    brand = models.CharField(max_length=100)
    color = models.ManyToManyField(Color)
    type = models.CharField(max_length=1, choices=TYPES)

    def __str__(self):
        return self.title + " | " + str(self.price) + " | " + str(self.amount) + " available"


class MultiPicture(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='pictures')
    picture = models.ImageField()

    def __str__(self):
        return self.product.title + " | " + str(self.product.price) + " | " + str(self.product.amount) + " available"


class Cloth(Product):
    size = models.ManyToManyField(Size)
    material = models.CharField(max_length=50)


class SportTool(Product):
    size = models.ManyToManyField(Size)

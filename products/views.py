from rest_framework.generics import ListCreateAPIView, ListAPIView

from products.models import Cloth, SportTool, Color, Size
from products.permissions import CreatePermission
from products.serializers import ClothSerializer, SportToolSerializer, SizeSerializer, ColorSerializer


class ClothListCreateAPIView(ListCreateAPIView):
    permission_classes = [CreatePermission]
    serializer_class = ClothSerializer

    def get_queryset(self):
        qs = Cloth.objects.all()

        price = self.request.GET.get('price')
        if price and len(price.split()) == 2:
            qs = qs.filter(price__gte=price.split()[0], price__lte=price.split()[1])

        brand = self.request.GET.get('brand')
        if brand:
            qs = qs.filter(brand__icontains=brand)

        colors = self.request.GET.get('colors')
        if colors:
            qs = qs.filter(color__name__in=colors.split())

        title = self.request.GET.get('title')
        if title:
            qs = qs.filter(title__icontains=title)

        return qs


class SportToolListCreateAPIView(ListCreateAPIView):
    permission_classes = [CreatePermission]
    serializer_class = SportToolSerializer

    def get_queryset(self):
        qs = SportTool.objects.all()

        price = self.request.GET.get('price')
        if price and len(price.split()) == 2:
            qs = qs.filter(price__gte=price.split()[0], price__lte=price.split()[1])

        brand = self.request.GET.get('brand')
        if brand:
            qs = qs.filter(brand__icontains=brand)

        colors = self.request.GET.get('colors')
        if colors:
            qs = qs.filter(color__name__in=colors.split())

        title = self.request.GET.get('title')
        if title:
            qs = qs.filter(title__icontains=title)

        return qs


class GetSizeAPIView(ListAPIView):
    queryset = Size.objects.all()
    serializer_class = SizeSerializer


class GetColorAPIView(ListAPIView):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer

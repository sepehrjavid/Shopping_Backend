from django.urls import path

from products.views import ClothListCreateAPIView, SportToolListCreateAPIView, GetColorAPIView, GetSizeAPIView

app_name = 'products'

urlpatterns = [
    path('cloth_list_create', ClothListCreateAPIView.as_view()),
    path('sport_tool_list_create', SportToolListCreateAPIView.as_view()),
    path('color_list', GetColorAPIView.as_view()),
    path('size_list', GetSizeAPIView.as_view())
]

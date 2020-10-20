from django.urls import path, re_path

from invoice.views import SubmitOrderAPIView, AddItemToCartAPIView, GetUserCartAPIView, RemoveOrderItemAPIView, \
    GetOrdersAPIView

app_name = 'invoice'

urlpatterns = [
    path('submit_order', SubmitOrderAPIView.as_view()),
    path('add_to_cart', AddItemToCartAPIView.as_view()),
    path('get_cart', GetUserCartAPIView.as_view()),
    path('get_orders', GetOrdersAPIView.as_view()),
    re_path(r'^remove_item/(?P<order_item_id>\d+)$', RemoveOrderItemAPIView.as_view()),
]

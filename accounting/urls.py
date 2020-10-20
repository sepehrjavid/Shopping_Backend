from django.urls import path

from accounting.views import CreateAccountAPIView, GetUserDataAPIView

app_name = 'accounting'

urlpatterns = [
    path('create_account', CreateAccountAPIView.as_view()),
    path('get_user_info', GetUserDataAPIView.as_view())
]

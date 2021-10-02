from django.urls import path
from api import views


urlpatterns = [
    # /api/
    path('', views.main_view),
    # /api/nasa/
    path('nasa/', views.receive_info_from_front),
]
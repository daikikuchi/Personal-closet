from django.urls import path
from .views import BrandListView

app_name = 'clothes'

urlpatterns = [
    path('brands/', BrandListView.as_view(), name='brand_list'),
]

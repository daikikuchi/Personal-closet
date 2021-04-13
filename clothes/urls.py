from django.urls import path
from .views import BrandListView, BrandClothesListView

app_name = 'clothes'

urlpatterns = [
    path('brands/', BrandListView.as_view(), name='brand_list'),
    path('brands/<int:id>/<slug:slug>/',
         BrandClothesListView.as_view(),
         name='brand_clothes'),
]

from django.urls import path
from .views import (BrandListView, BrandClothesListView, CategoryListView,
                    CategoryClothesListView)

app_name = 'clothes'

urlpatterns = [
    # Brands URLS
    path('brand/', BrandListView.as_view(), name='brand_list'),
    path('brand/<int:id>/<slug:slug>/',
         BrandClothesListView.as_view(),
         name='brand_clothes'),

    # Category URLS
    path('category/', CategoryListView.as_view(), name='category_list'),
    path('category/<int:id>/<slug:slug>/',
         CategoryClothesListView.as_view(),
         name='category_clothes'),
]

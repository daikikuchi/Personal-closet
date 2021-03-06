from django.urls import path
from .views import (BrandListView, BrandClothesListView, CategoryListView,
                    CategoryClothesListView, ShopListView, ShopClothesView,
                    ClothesDetailView, ClothesSearchResultsListView)

app_name = 'clothes'

urlpatterns = [

    # Clothes detail URLS
    path('<int:pk>/', ClothesDetailView.as_view(), name='clothes_detail'),
    path('search/',
         ClothesSearchResultsListView.as_view(),
         name='search_results'),

    # Brands URLS
    path('brand/', BrandListView.as_view(), name='brand_list'),
    path('brand/<int:id>/<slug:slug>/',
         BrandClothesListView.as_view(),
         name='brand_clothes'),

    # Category URLS
    path('category/', CategoryListView.as_view(), name='category_list'),
    path('category/<slug:slug>/',
         CategoryClothesListView.as_view(),
         name='category_clothes'),

    # Shop URLS
    path('shop/', ShopListView.as_view(), name='shop_list'),
    path('shop/<slug:slug>/', ShopClothesView.as_view(), name='shop_clothes'),
]

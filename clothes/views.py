from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Brand, Clothes, Category, Shop


class OwnerMixin(ListView):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)


class BrandListView(LoginRequiredMixin, OwnerMixin):
    model = Brand
    context_object_name = 'brand_list'
    template_name = 'brand/brand_list.html'


class BrandClothesListView(LoginRequiredMixin, OwnerMixin):
    model = Clothes
    context_object_name = 'brand_clothes_list'
    template_name = 'brand/brand_clothes_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(brand=self.kwargs.get('id'))


class CategoryListView(LoginRequiredMixin, OwnerMixin):
    model = Category
    context_object_name = 'category_list'
    template_name = 'category/category_list.html'


class CategoryClothesListView(LoginRequiredMixin, OwnerMixin):
    model = Clothes
    context_object_name = 'category_clothes_list'
    template_name = 'category/category_clothes_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return (queryset.
                filter(sub_category__category__slug=self.kwargs.get('slug')))


class ShopListView(LoginRequiredMixin, OwnerMixin):
    model = Shop
    context_object_name = 'shop_list'
    template_name = 'shop/shop_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('name')


class ShopClothesView(LoginRequiredMixin, OwnerMixin):
    model = Clothes
    context_object_name = 'shop_clothes_list'
    template_name = 'shop/shop_clothes_list.html'

    def get_queryset(self):
        shop = get_object_or_404(Shop, slug=self.kwargs.get('slug'))
        queryset = super().get_queryset()
        return queryset.select_related('shop').filter(shop=shop.id)

from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404

from .models import Brand, Clothes


class OwnerMixin(ListView):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user).order_by('-name').distinct()


class BrandListView(LoginRequiredMixin, OwnerMixin):
    model = Brand
    context_object_name = 'brand_list'
    template_name = 'brand/brand_list.html'


class BrandClothesListView(LoginRequiredMixin, ListView):
    model = Clothes
    context_object_name = 'brand_clothes_list'
    template_name = 'brand/brand_clothes_list.html'

    def get_queryset(self):
        try:
            clothes = (Clothes.objects.select_related('brand')
                       .filter(brand=self.kwargs.get('id'),
                       user=self.request.user))
        except Brand.DoesNotExist:
            raise Http404
        else:
            return clothes

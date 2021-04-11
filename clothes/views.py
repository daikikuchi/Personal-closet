from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Brand


class OwnerMixin(object):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user).order_by('-name').distinct()


class BrandListView(LoginRequiredMixin, ListView, OwnerMixin):
    model = Brand
    context_object_name = 'brand_list'
    template_name = 'brand/brand_list.html'


from distutils.sysconfig import customize_compiler
from msilib.schema import ListView
from django.shortcuts import render, redirect
from urllib import request
from urllib.request import Request
from django.views.generic import TemplateView, View, ListView, CreateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin
from .models import *
from eccomapp.models import *
from django.urls import reverse_lazy
# Create your views here.


class SuperUserCheck(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser


class AdminRequiredMixin(object):
    def dispatch(self, *args, **kwargs):
        if request.user.is_authenticated and Admin.objects.filter(user=request.user).exists():
            pass
        else:
            return redirect("/admin-login/")
        return super().dispatch(request, *args, **kwargs)


class ReportView(TemplateView):
    template_name = 'pending-order.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pendingorders"] = Order.objects.filter(
            order_status="Order Received").order_by("-id")

        return context


class UserReportListView(ListView):
    model = Customer
    context_object_name = 'cust'
    template_name = 'UserReport.html'


class OrderReportListView(ListView):
    context_object_name = 'ord'
    queryset = Order.objects.all()
    template_name = 'order_report_list_view.html'


class OrderReportDetailView(DetailView):
    template_name = "orderdetail.html"
    model = Order
    context_object_name = "ord_obj"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["allstatus"] = ORDER_STATUS
        return context


class ProductReportListView(ListView):
    model = Product
    context_object_name = "pro"
    template_name = 'productreport.html'


class ProductReportUpdateView(UpdateView):
    model = Product
    fields = '__all__'
    template_name = "productedit.html"
    success_url = reverse_lazy('reports:product')


class ProductDeleteView(SuperUserCheck, DeleteView):
    template_name = "deleteproduct.html"
    model = Product
    success_url = reverse_lazy('reports:product')


class ProductCreateView(SuperUserCheck, CreateView):
    template_name = "createproduct.html"
    model = Product
    fields = '__all__'
    success_url = reverse_lazy('reports:product')


class CartproductListView(ListView):
    model = CartProduct
    context_object_name = 'cp'
    template_name = 'cart_product_list_view.html'

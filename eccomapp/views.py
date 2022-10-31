from cProfile import Profile
from multiprocessing import context, get_context
from os import supports_dir_fd
import profile
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, View, CreateView, DeleteView
from django.views.generic.edit import UpdateView, DeleteView
from .models import *
from django.urls import reverse_lazy
from .forms import CheckoutForm, CustomerRegisterationForm


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_list'] = Product.objects.all().order_by("-id")
        return context


class AllProductsView(TemplateView):
    template_name = "allproducts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['allcategories'] = Category.objects.all()
        return context


class ProductDetailView(LoginRequiredMixin, TemplateView):
    template_name = "productdetail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs['slug']
        product = Product.objects.get(slug=slug)
        product.view_count += 1
        product.save()
        context['product'] = product
        return context


class AddToCartView(LoginRequiredMixin, TemplateView):
    template_name = "addtocart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get productid form requested url
        product_id = self.kwargs['pro_id']
        # get product
        product_obj = Product.objects.get(id=product_id)

        # check if cart exists
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            this_product_in_cart = cart_obj.cartproduct_set.filter(
                product=product_id)
            if this_product_in_cart.exists():
                cartproduct = this_product_in_cart.last()
                cartproduct.quantity += 1
                cartproduct.subtotal += product_obj.selling_price
                cartproduct.save()
                cart_obj.total += product_obj.selling_price
                cart_obj.save()
            else:
                cartproduct = CartProduct.objects.create(
                    cart=cart_obj, product=product_obj, rate=product_obj.selling_price, quantity=1, subtotal=product_obj.selling_price)
                cart_obj.total += product_obj.selling_price
                cart_obj.save()
        else:
            cart_obj = Cart.objects.create(total=0)
            self.request.session['cart_id'] = cart_obj.id
            cartproduct = CartProduct.objects.create(
                cart=cart_obj, product=product_obj, rate=product_obj.selling_price, quantity=1, subtotal=product_obj.selling_price)
            cart_obj.total += product_obj.selling_price
            cart_obj.save()
        return context


class ManageCartView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        cp_id = self.kwargs["cp_id"]
        action = request.GET.get("action")
        cp_obj = CartProduct.objects.get(id=cp_id)
        cart_obj = cp_obj.cart
        if action == "inc":
            cp_obj.quantity += 1
            cp_obj.subtotal += cp_obj.rate
            cp_obj.save()
            cart_obj.total += cp_obj.rate
            cart_obj.save()
        elif action == "dcr":
            cp_obj.quantity -= 1
            cp_obj.subtotal -= cp_obj.rate
            cp_obj.save()
            cart_obj.total -= cp_obj.rate
            cart_obj.save()
            if cp_obj.quantity == 0:
                cp_obj.delete()
        elif action == "rmv":
            cart_obj.total
            cart_obj.save()
            cp_obj.delete()
        else:
            pass
        return redirect("eccomapp:mycart")


class MyCartView(LoginRequiredMixin, TemplateView):
    template_name = "mycart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            cart = Cart.objects.get(id=cart_id)
            cart_obj.customer = self.request.user.customer
            cart_obj.save()
        else:
            cart = None
        context['cart'] = cart
        return context


class EmptyCartView(View):
    def get(self, request, *args, **kwargs):
        cart_id = request.session.get("cart_id", None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
            cart.cartproduct_set.all().delete()
            cart.total = 0
            cart.save()
        return redirect("eccomapp:mycart")


class CheckOutView(LoginRequiredMixin, CreateView):
    template_name = "checkout.html"
    form_class = CheckoutForm
    success_url = reverse_lazy("eccomapp:ordersucess")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.customer:
            pass
        else:
            return redirect("/login/?next=/checkout/")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
        else:
            cart_obj = None
        context["cart"] = cart_obj
        return context

    def form_valid(self, form):
        cart_id = self.request.session.get("cart_id")
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            form.instance.cart = cart_obj
            form.instance.subtotal = cart_obj.total
            form.instance.discount = 0
            form.instance.total = cart_obj.total
            form.instance.order_status = "Order Received"
            del self.request.session['cart_id']
        else:
            return redirect("eccomapp:home")
        return super().form_valid(form)


class SuccessOrderView(TemplateView):
    template_name = 'success-order.html'


class CustomerOrderView(TemplateView):
    template_name = 'customer/profile.html'
    model = Order
    context_object_name = "orders"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = Order.objects.all()
        return context


class DeleteOrder(DeleteView):
    template_name = "order_confirm_delete.html"
    model = Order
    success_url = reverse_lazy("eccomapp:home")


class RegisterPage(CreateView):
    template_name = "customers/register.html"
    form_class = CustomerRegisterationForm
    success_url = reverse_lazy("eccomapp:login")

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        email = form.cleaned_data.get("email")
        user = User.objects.create_user(username, email, password)
        form.instance.user = user
        login(self.request, user)
        return super().form_valid(form)


class CustomerLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("eccomapp:home")


class LoginView(LoginView):
    template_name = 'customers/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("eccomapp:home")

    def get_success_url(self):
        if "next" in self.request.GET:
            next_url = self.request.GET.get("next")
            return (next_url)
        else:
            return reverse_lazy("eccomapp:home")


class CustomerProfile(TemplateView):
    template_name = 'customers/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = self.request.user.customer
        context["customer"] = customer
        orders = Order.objects.filter(cart__customer=customer)
        context['orders'] = orders
        return context


class CustomerOrderDetailView(DeleteView):
    template_name = "customers/Orderdetails.html"
    model = Order
    context_object_name = "ord_obj"


class ProfileUpdateView(UpdateView):
    template_name = "customers/profileupdate.html"
    model = Profile
    fields = '__all__'
    success_ur = reverse_lazy("eccomapp:profile")


class CustomerProfileCreateView(CreateView):
    model = Profile
    fields = ['bio', 'image']
    template_name = 'customers/createprofil.html'
    success_url = reverse_lazy('eccomapp:home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)


class AboutView(TemplateView):
    template_name = "about.html"


class ContactView(TemplateView):
    template_name = "contact.html"
# Create your views here.

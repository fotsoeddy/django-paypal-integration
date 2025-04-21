from django.views.generic import TemplateView, RedirectView
from paypal.standard.forms import PayPalPaymentsForm
from django.urls import reverse
from django.conf import settings
from .models import Project

class ProjectListView(TemplateView):
    template_name = 'payments/project_list.html'

class CheckoutView(TemplateView):
    template_name = 'payments/checkout.html'

class PaymentSuccessView(TemplateView):
    template_name = 'payments/payment_success.html'

class PaymentFailedView(TemplateView):
    template_name = 'payments/payment_failed.html'
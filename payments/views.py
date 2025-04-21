from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from .models import Project
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
from django.urls import reverse
from uuid import uuid4

class ProjectListView(TemplateView):
    template_name = 'payments/project_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = Project.objects.all()
        return context

class CheckoutView(TemplateView):
    template_name = 'payments/checkout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_id = self.kwargs.get('pk')
        project = get_object_or_404(Project, id=project_id)
        host = self.request.get_host()
        paypal_checkout = {
            'business': settings.PAYPAL_RECEIVER_EMAIL,
            'amount': project.price.amount,
            'item_name': project.name,
            'invoice': str(uuid4()),
            'currency_code': project.price.currency,
            'notify_url': f"{self.request.scheme}://{host}{reverse('paypal-ipn')}",
            'return_url': f"{self.request.scheme}://{host}{reverse('payments:payment_success', kwargs={'pk': project_id})}",
            'cancel_url': f"{self.request.scheme}://{host}{reverse('payments:payment_failed', kwargs={'pk': project_id})}",
        }
        paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)
        context['project'] = project
        context['paypal'] = paypal_payment
        return context

class PaymentSuccessView(TemplateView):
    template_name = 'payments/payment_success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_id = self.kwargs.get('pk')
        context['project'] = get_object_or_404(Project, id=project_id)
        return context

class PaymentFailedView(TemplateView):
    template_name = 'payments/payment_failed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_id = self.kwargs.get('pk')
        context['project'] = get_object_or_404(Project, id=project_id)
        return context
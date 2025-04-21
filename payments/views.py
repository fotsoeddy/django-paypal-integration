from django.views.generic import TemplateView, ListView
from django.shortcuts import get_object_or_404
from .models import Project, Transaction
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
from django.urls import reverse
from uuid import uuid4
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse
import base64
import zlib
import requests
import logging
import json
from datetime import datetime
from dateutil.parser import parse
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

# Set up logging
logger = logging.getLogger(__name__)

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
            'amount': f"{project.price.amount:.2f}",
            'item_name': project.name,
            'invoice': str(uuid4()),
            'currency_code': str(project.price.currency),
            'notify_url': f"{self.request.scheme}://{host}{reverse('payments:paypal-webhook')}",
            'return_url': f"{self.request.scheme}://{host}{reverse('payments:payment_success', kwargs={'pk': project_id})}",
            'cancel_url': f"{self.request.scheme}://{host}{reverse('payments:payment_failed', kwargs={'pk': project_id})}",
            'custom': str(project_id),
        }
        logger.debug(f"PayPal checkout data: {paypal_checkout}")
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

class TransactionListView(ListView):
    model = Transaction
    template_name = 'payments/transaction_list.html'
    context_object_name = 'transactions'

@csrf_exempt
@require_POST
def PayPalWebhookView(request):
    body = request.body
    logger.debug(f"Webhook received: {body}")
    # Extract headers for verification
    transmission_id = request.headers.get("paypal-transmission-id")
    timestamp = request.headers.get("paypal-transmission-time")
    webhook_id = settings.PAYPAL_WEBHOOK_ID
    cert_url = request.headers.get("paypal-cert-url")
    signature = request.headers.get("paypal-transmission-sig")

    # Calculate CRC32 of the body
    crc = zlib.crc32(body)
    message = f"{transmission_id}|{timestamp}|{webhook_id}|{crc}"

    # Fetch and cache certificate
    try:
        r = requests.get(cert_url)
        certificate = r.text
    except requests.RequestException as e:
        logger.error(f"Failed to fetch certificate: {e}")
        return HttpResponse(status=400)

    # Verify signature
    try:
        cert = x509.load_pem_x509_certificate(certificate.encode("utf-8"), default_backend())
        public_key = cert.public_key()
        signature = base64.b64decode(signature)
        public_key.verify(
            signature,
            message.encode("utf-8"),
            padding.PKCS1v15(),
            hashes.SHA256()
        )
    except Exception as e:
        logger.error(f"Signature verification failed: {e}")
        return HttpResponse(status=400)

    # Process webhook event
    try:
        payload = json.loads(body)
        event_type = payload.get("event_type")
        logger.debug(f"Webhook event type: {event_type}")
        if event_type == "PAYMENT.SALE.COMPLETED":
            resource = payload.get("resource", {})
            project_id = resource.get("custom_id")
            transaction_id = resource.get("id")
            amount = resource.get("amount", {}).get("total")
            currency = resource.get("amount", {}).get("currency")
            invoice_id = resource.get("invoice_number", "")
            status = resource.get("state", "unknown")
            created_at = parse(payload.get("create_time", datetime.now().isoformat()))

            # Log transaction details
            logger.info(
                f"Transaction Details: ID={transaction_id}, Project ID={project_id}, "
                f"Amount={amount} {currency}, Invoice={invoice_id}, Status={status}, Created={created_at}"
            )

            # Save to Transaction model
            if project_id and amount and currency:
                try:
                    project = Project.objects.get(id=project_id)
                    Transaction.objects.update_or_create(
                        transaction_id=transaction_id,
                        defaults={
                            'project': project,
                            'amount': (amount, currency),
                            'invoice_id': invoice_id,
                            'status': status,
                            'created_at': created_at,
                            'raw_data': payload,
                        }
                    )
                    project.status = 'purchased'
                    project.save()
                    logger.info(f"Project {project_id} marked as purchased")
                except Project.DoesNotExist:
                    logger.error(f"Project {project_id} not found")
            else:
                logger.warning(f"Incomplete transaction data: {payload}")
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON payload: {e}")
        return HttpResponse(status=400)

    return HttpResponse(status=200)
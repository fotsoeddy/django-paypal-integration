from django.conf import settings

def project_context(request):
    return {
        'paypal_receiver_email': settings.PAYPAL_RECEIVER_EMAIL,
        'paypal_button_image': settings.PAYPAL_BUY_BUTTON_IMAGE,
    }
# from django.dispatch import receiver
# from paypal.standard.models import ST_PP_COMPLETED
# from paypal.standard.ipn.signals import valid_ipn_received

# @receiver(valid_ipn_received)
# def paypal_payment_received(sender, **kwargs):
#     ipn_obj = sender
#     if ipn_obj.payment_status == ST_PP_COMPLETED:
#         project_id = ipn_obj.custom
#         # Add logic to mark project as purchased if needed
#         pass
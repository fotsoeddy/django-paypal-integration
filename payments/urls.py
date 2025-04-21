from django.urls import path
from . import views
from paypal.standard.ipn import views as paypal_views

app_name = 'payments'

urlpatterns = [
    path('', views.ProjectListView.as_view(), name='project_list'),
    path('checkout/<int:pk>/', views.CheckoutView.as_view(), name='checkout'),
    path('payment/success/<int:pk>/', views.PaymentSuccessView.as_view(), name='payment_success'),
    path('payment/failed/<int:pk>/', views.PaymentFailedView.as_view(), name='payment_failed'),
    path('paypal/', paypal_views.ipn, name='paypal-ipn'),
]
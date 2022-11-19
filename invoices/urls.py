from django.urls import path
from .views import InvoiceView

urlpatterns = [
    path('invoices', InvoiceView.as_view(), name='invoices_list'),
    path('invoices/<int:id>', InvoiceView.as_view(), name='invoices_process')
]
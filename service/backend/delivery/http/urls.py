from django.urls import path
from delivery.http.views import create_deliverer, update_deliverer_status, assign_order, reassign_order

urlpatterns = [
    path('deliverers/', create_deliverer, name='create-deliverer'),
    path('deliverers/<uuid:deliverer_id>/status/',
         update_deliverer_status, name='update-deliverer-status'),
    path('orders/assign/', assign_order, name='assign-order'),
    path('orders/<uuid:order_id>/reassign/',
         reassign_order, name='reassign-order'),
]

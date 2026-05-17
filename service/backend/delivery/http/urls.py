from django.urls import path
from service.backend.delivery.http.views.deliverers_views import deliverers_collection, update_deliverer_status, assign_order, reassign_order
from service.backend.delivery.http.views.pagamento_views import AplicarCupomView, ComprovanteView, EstornarPagamentoView, MetodoPagamentoDetailView, MetodosPagamentoView, ProcessarPagamentoView

urlpatterns = [
    path('deliverers/', deliverers_collection, name='deliverers-collection'),
    path('deliverers/<uuid:deliverer_id>/status/',
         update_deliverer_status, name='update-deliverer-status'),
    path('orders/assign/', assign_order, name='assign-order'),
    path('orders/<uuid:order_id>/reassign/',
         reassign_order, name='reassign-order'),

     # Métodos de pagamento
    path('api/pagamento/metodos', MetodosPagamentoView.as_view()),
    path('api/pagamento/metodos/<int:metodo_id>', MetodoPagamentoDetailView.as_view()),
    
    # Cupons
    path('api/pagamento/aplicar-cupom', AplicarCupomView.as_view()),
    
    # Pagamento
    path('api/pagamento/processar/<str:pedido_id>', ProcessarPagamentoView.as_view()),
    path('api/pagamento/estornar/<str:pedido_id>', EstornarPagamentoView.as_view()),
    
    # Comprovante
    path('api/pagamento/comprovante/<str:pedido_id>', ComprovanteView.as_view())
]

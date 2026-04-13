from django.urls import path, include

urlpatterns = [
    path('api/', include('delivery.http.urls')),
]

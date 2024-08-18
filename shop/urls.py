from django.urls import path
from shop.views import home, index, detail, checkout, confimation
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name='home'),
    path('billeterie/', index, name='index'),
    path('<int:myid>', detail, name="detail"),
    path('checkout', checkout, name="checkout"),
    path('confirmation', confimation, name="confirmation" ),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


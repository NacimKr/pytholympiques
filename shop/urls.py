from django.urls import path
from shop.views import home, index, detail, checkout, confimation, create_account_user, account_user, login_account_user
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name='home'),
    path('billeterie/', index, name='index'),
    path('billeterie/<int:myid>', detail, name="detail"),
    path('billeterie/checkout', checkout, name="checkout"),
    path('billeterie/confirmation', confimation, name="confirmation" ),
    path('billeterie/creation_compte', create_account_user, name="creation_compte" ),
    path('billeterie/connexion_compte', login_account_user, name="connexion_compte" ),
    path('billeterie/page_de_connexion', account_user, name="account_user" ),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


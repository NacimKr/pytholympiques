from django.urls import path
from shop.views import home, index, detail, success_payment, get_number_product_in_cart, create_product ,checkout, logout_account_user, add_cart, payment, confimation, create_account_user, account_user, login_account_user, delete_cart, delete_cart_by_id
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name='home'),
    path('billeterie/', index, name='index'),
    path('billeterie/create_product', create_product, name='create_product'),
    path('billeterie/<int:myid>', detail, name="detail"),
    path('billeterie/add_cart/<int:myid>', add_cart, name="add_cart"),
    path('billeterie/checkout', checkout, name="checkout"),
    path('billeterie/confirmation', confimation, name="confirmation" ),
    path('billeterie/creation_compte', create_account_user, name="creation_compte" ),
    path('billeterie/connexion_compte', login_account_user, name="connexion_compte" ),
    path('billeterie/delete_cart', delete_cart, name="delete_cart" ),
    path('billeterie/delete_cart/<int:id>', delete_cart_by_id, name="delete_cart_by_id" ),
    path('billeterie/deconnexion', logout_account_user, name="logout" ),
    path('billeterie/page_de_connexion', account_user, name="account_user" ),
    path('billeterie/paiement', payment, name="payment" ),
    path('billeterie/success_paiement', success_payment, name="success_payment" ),
    path('billeterie/get_number_product_in_cart', get_number_product_in_cart, name="get_number_product_in_cart" ),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


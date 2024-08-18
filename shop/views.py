from django.shortcuts import redirect, render
from .models import Product, Commande
from django.core.paginator import Paginator
from key_generator.key_generator import generate


# Create your views here.
def home(request):
    return render(request, 'shop/home.html')


def index(request):
    print(request.user)
    product_object = Product.objects.all()
    item_name = request.GET.get('item-name')
    if item_name !='' and item_name is not None:
        product_object = Product.objects.filter(title__icontains=item_name)
    paginator = Paginator(product_object, 4)
    page = request.GET.get('page')
    product_object = paginator.get_page(page)
    return render(request, 'shop/index.html', {'product_object': product_object})


def detail(request, myid):
    product_object = Product.objects.get(id=myid)
    return render(request, 'shop/detail.html', {'product': product_object}) 


def checkout(request):
    if request.method == "POST":
        items = request.POST.get('items')
        total = request.POST.get('total')
        nom = request.POST.get('nom')
        email = request.POST.get('email')
        address = request.POST.get('address')
        ville = request.POST.get('ville')
        pays = request.POST.get('pays')
        zipcode= request.POST.get('zipcode')
        com = Commande(items=items,total=total, nom=nom, email=email, address=address, ville=ville, pays=pays, zipcode=zipcode)
        com.save()
        return redirect('confirmation')
    return render(request, 'shop/checkout.html') 


def create_account_user(request):
    key = generate(seed = 101)
    userName = request.POST.get('complet_name', None)
    userPass = request.POST.get('mot_de_passe', None)
    userId = request.POST.get('identifiant', None)
    print(userName)
    print(userPass)
    print(userId)
    print(key.get_key())
    return render(request, 'shop/create_user.html') 



def confimation(request):
    info = Commande.objects.all()[:1]
    for item in info:
        nom = item.nom
    return render(request, 'shop/confirmation.html', {'name': nom})          
from django.shortcuts import redirect, render
from .models import Product, Commande
from django.core.paginator import Paginator
from key_generator.key_generator import generate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login

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
        com = Commande(
            items=items,
            total=total, 
            nom=nom, 
            email=email, 
            address=address, 
            ville=ville, 
            pays=pays, 
            zipcode=zipcode
        )
        com.save()
        return redirect('confirmation')
    return render(request, 'shop/checkout.html') 


def create_account_user(request):
    if request.method == "POST":
        key = generate(seed = 101)
        userName = request.POST.get('username', None)
        userPass = request.POST.get('password1', None)
        userPassConfirm = request.POST.get('password2', None)
        print(userName)
        print(userPass)
        print(userPassConfirm)
        print(key.get_key())
        if userPass == userPassConfirm:
            try:
                user = User.objects.create_user(username=userName, password=userPass)
                user.save()
                login(request, user)
                return redirect("account_user")
            except IntegrityError:
                return render(
                    request, 
                    'shop/create_user.html', 
                    {
                        "form": UserCreationForm,
                        "erreur": "Cet utilisateur est déjà inscrit"
                    }
                ) 
        else:
            return render(
                request, 
                'shop/create_user.html', 
                {
                    "form": UserCreationForm,
                    "erreur" : "Les mots de passe ne sont pas identiques"
                }
            ) 
    else:
        return render(request, 'shop/create_user.html', {"form": UserCreationForm}) 



def account_user(request):
    return render(request, "shop/account_user.html")



def login_account_user(request):
    pass



def confimation(request):
    info = Commande.objects.all()[:1]
    for item in info:
        nom = item.nom
    return render(request, 'shop/confirmation.html', {'name': nom})          
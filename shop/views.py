from django.shortcuts import redirect, render, get_object_or_404
from .models import Product, User, Order, Cart
from django.core.paginator import Paginator
from key_generator.key_generator import generate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import IntegrityError
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages

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
        pass
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


def logout_account_user(request):
    logout(request)
    return redirect("connexion_compte")



def login_account_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, 'shop/account_user.html')
        else:
            messages.info(request, "Les identifiants sont incorrect")
    form = AuthenticationForm()
    return render(request, "shop/login.html", {"form":form})


def add_cart(request, myid):
    user = request.user
    product = get_object_or_404(Product, id=myid)
    panier_cart, _ = Cart.objects.get_or_create(user=user)
    order, created = Order.objects.get_or_create(user=user, product=product)
    
    if created:
        panier_cart.orders.add(order)
        panier_cart.save()
    else:
        order.quantity += 1
        order.save()
        
    return redirect("index")


def confimation(request):
    info = Product.objects.all()[:1]
    for item in info:
        nom = item.nom
    return render(request, 'shop/confirmation.html', {'name': nom})          
from django.shortcuts import redirect, render, get_object_or_404
from django.http import JsonResponse
from .models import Product, User, Order, Cart
from django.core.paginator import Paginator
from key_generator.key_generator import generate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import IntegrityError
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import ProductForm
from .forms import UserForm


""" Methode pour afficher la page d'accueil """
def home(request):
    return render(request, 'shop/home.html')


""" Methode pour créer un produit en tant qu'administrateur """
def create_product(request):
    if request.method == "POST":
        new_product = Product.objects.create(
            title = request.POST.get("title"),
            price = request.POST.get("price"),
            description = request.POST.get("description"),
            image = request.POST.get("image"),
            quantity = request.POST.get("quantity"),
        )
        new_product.save()
        # print(new_product)
        # print(type(new_product))
        return redirect("index")
    return render(request,"shop/create_product.html",{"productForm":ProductForm})


""" Methode pour modifier un produit en tant qu'administrateur """
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('index')  # Redirige vers la liste des produits ou une autre vue
    else:
        form = ProductForm(instance=product)

    return render(request, 'shop/edit_product.html', {'form': form})


""" Methode pour supprimer un produit quand on est l'administrateur """
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('index')


""" Methode pour afficher tous les produit en base """
def index(request):
    print(request.user)
    product_object = Product.objects.all()
    item_name = request.GET.get('item-name')
    if item_name !='' and item_name is not None:
        product_object = Product.objects.filter(title__icontains=item_name)
    paginator = Paginator(product_object, 4)
    page = request.GET.get('page')
    product_object = paginator.get_page(page)
    
    total_prix = 0
    order_user = Order.objects.all()
        
    if not request.user.is_anonymous:
        order_user = Order.objects.filter(user=request.user)
    
    for order in order_user:
        total_prix += order.quantity * order.product.price

    print(order_user)
        
    return render(request, 'shop/index.html', {'product_object': product_object, "order_user":order_user, "total" : total_prix})


""" Methode pour afficher le details du produit en base """
def detail(request, myid):
    product_object = Product.objects.get(id=myid)
    return render(request, 'shop/detail.html', {'product': product_object}) 


def checkout(request):
    if request.method == "POST":
        pass
        return redirect('confirmation')
    
    order_user = Order.objects.filter(user=request.user)
    print(type(order_user))
    print(order_user)
    total_prix = 0
    
    for order in order_user:
        total_prix += order.quantity * order.product.price
    return render(request, 'shop/checkout.html', {"order_user":order_user, "total" : total_prix}) 


""" Methode pour gérer la création d'un compte utilisateur """
def create_account_user(request):
    if request.method == "POST":
        key = generate(seed = 101)
        userName = request.POST.get('username', None)
        userPass = request.POST.get('password1', None)
        userPassConfirm = request.POST.get('password2', None)
        firstName = request.POST.get('first_name', None)
        lastName = request.POST.get('last_name', None)
        email = request.POST.get('email', None)
        userPassConfirm = request.POST.get('password2', None)
        if userPass == userPassConfirm:
            try:
                user = User.objects.create_user(
                    username=userName, 
                    last_name=lastName, 
                    first_name=firstName,
                    email=email, 
                    password=userPass,
                    key_generate=key.get_key()
                )
                user.save()
                login(request, user)
                return redirect("account_user")
            except IntegrityError:
                return render(
                    request, 
                    'shop/create_user.html', 
                    {
                        "form": UserForm,#UserCreationForm,
                        "erreur": "Cet utilisateur est déjà inscrit"
                    }
                ) 
        else:
            return render(
                request, 
                'shop/create_user.html', 
                {
                    "form": UserForm, #UserCreationForm,
                    "erreur" : "Les mots de passe ne sont pas identiques"
                }
            ) 
    else:
        return render(request, 'shop/create_user.html', {"form":  UserForm}) #UserCreationForm, 


""" Methode pour afficher la page de l'utilisateur une fois connecter """
def account_user(request):
    return render(request, "shop/account_user.html")


""" Methode pour déconnecter l'utilisateur """
def logout_account_user(request):
    logout(request)
    return redirect("connexion_compte")


""" Methode pour savoir combien de produit l'utilisateur a dans son panier """
def get_number_product_in_cart(request):
    if request.method == "POST":
        number_cart = request.POST.get("panier_product_quantity")
        nb_product = int(list(request.POST.keys())[0])
        return JsonResponse({ 'status': 'success', 'number_cart': int(list(request.POST.keys())[0]), })



""" Methode pour connecter l'utilisateur """
def login_account_user(request):
    if request.method == "POST" :
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            order_user = Order.objects.filter(user=request.user)
            total_prix = 0
            for order in order_user:
                total_prix += order.quantity * order.product.price
            return render(request, 'shop/account_user.html',{"order_user":order_user, "total" : total_prix})
        else:
            messages.info(request, "Les identifiants sont incorrect")
    form = AuthenticationForm()
    return render(request, "shop/login.html", {"form":form})
    

""" Methode pour ajouter un produit dans le panier """
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


""" Methode pour supprimer les produits dans le panier """
def delete_cart(request):
    if cart := request.user.cart:
        cart.orders.all().delete()
        cart.delete()
    return redirect("index")


""" Methode pour supprimer les produits dans le panier """
def delete_cart_by_id(request, id):
    if cart := request.user.cart:
        cart.orders.filter(id=id).delete()
        cart.delete()
    return redirect("index")


""" Methode pour supprimer les produits dans le panier pour l'utilisateur non connecté """
def delete_cart_by_id_no_connect(request, id):
    Cart.orders.filter(id=id).delete()
    Cart.delete()
    return redirect("index")


""" Methode pour afficher la page de confirmation de commande """
def confimation(request):
    info = Product.objects.all()[:1]
    return render(request, 'shop/confirmation.html')          


""" Methode pour afficher la page de paiement """
def payment(request):
    return render(request, 'shop/payment.html')          


""" Methode pour afficher la page de succèes de """
def success_payment(request):
    key = generate(seed = 101)
    print(key.get_key())
    if request.method == "POST" and request.session.get("nb") is not None:
        for i in range(1,int(request.session.get("nb"))+1):
            new_product = Order.objects.create(
                user = User.objects.get(username=request.user),
                product = Product.objects.get(
                    title=request.POST["nom-"+str(i)]
                ),
                quantity = request.POST["quantite-"+str(i)],
                ordered = True,
                key_generate_order = key.get_key()
            )
            new_product.save()

    return render(request, 'shop/success_payment.html')          
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



nb_product = None

def home(request):
    return render(request, 'shop/home.html')



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
        print(new_product)
        print(type(new_product))
        return redirect("index")
    return render(request,"shop/create_product.html",{"productForm":ProductForm})



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
    
    print("-------------------------------------")
    print(request.user)
    print(type(request.user))
    print("-------------------------------------")

    
    if not request.user.is_anonymous:
        order_user = Order.objects.filter(user=request.user)
    
    for order in order_user:
        total_prix += order.quantity * order.product.price

    print(order_user)
        
    return render(request, 'shop/index.html', {'product_object': product_object, "order_user":order_user, "total" : total_prix})



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



def create_account_user(request):
    if request.method == "POST":
        key = generate(seed = 101)
        userName = request.POST.get('username', None)
        userPass = request.POST.get('password1', None)
        userPassConfirm = request.POST.get('password2', None)
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



def get_number_product_in_cart(request):
    if request.method == "POST":
        number_cart = request.POST.get("panier_product_quantity")
        nb_product = int(list(request.POST.keys())[0])
        request.session["nb"] = int(list(request.POST.keys())[0])
        print("-----------------------------------------------------")
        print("Votre session a bien été créer")
        print("-----------------------------------------------------")
        return JsonResponse({ 'status': 'success', 'number_cart': int(list(request.POST.keys())[0]), })




def login_account_user(request):
    if request.method == "POST" and request.user:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            ######
            order_user = Order.objects.filter(user=request.user)
            total_prix = 0
            for order in order_user:
                total_prix += order.quantity * order.product.price
            return render(request, 'shop/account_user.html',{"order_user":order_user, "total" : total_prix})
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



def delete_cart(request):
    if cart := request.user.cart:
        cart.orders.all().delete()
        cart.delete()
    return redirect("index")



def delete_cart_by_id(request, id):
    if cart := request.user.cart:
        cart.orders.filter(id=id).delete()
        cart.delete()
    return redirect("index")



def delete_cart_by_id_no_connect(request, id):
    Cart.orders.filter(id=id).delete()
    Cart.delete()
    return redirect("index")



def confimation(request):
    info = Product.objects.all()[:1]
    return render(request, 'shop/confirmation.html')          



def payment(request):
    # print(int(request.session.get("nb")))
    return render(request, 'shop/payment.html')          



def success_payment(request):
    #print(int(request.session.get("nb")))
    if request.method == "POST":
        for i in range(1,int(request.session.get("nb"))+1):
            print(i)
            new_product = Order.objects.create(
                user = User.objects.get(username=request.user),
                product = Product.objects.get(
                    title=request.POST["nom-"+str(i)]
                ),
                quantity = request.POST["quantite-"+str(i)],
                ordered = True
            )
            new_product.save()

    return render(request, 'shop/success_payment.html')          
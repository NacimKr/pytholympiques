from django.contrib import admin
from .models import Category, Product, Commande, User

# Register your models here.
admin.site.site_header = "Billeterie Jeux Olympiques 2024"
admin.site.site_title = "Jeux Olympiques 2024"
admin.site.index_title = "Administration JO 2024"

class AdminCategorie(admin.ModelAdmin):
    list_display = ('name', 'date_added')

class AdminProduct(admin.ModelAdmin):
    list_display = ('title', 'price', 'category', 'date_added')
    search_fields = ('title',) 
    list_editable = ('price',)

class AdminCommande(admin.ModelAdmin):
    list_display = ('items','nom','email','address', 'ville', 'pays','total', 'date_commande', )

admin.site.register(Product, AdminProduct)
admin.site.register(Category, AdminCategorie)
admin.site.register(Commande, AdminCommande)
admin.site.register(User)

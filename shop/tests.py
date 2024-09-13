from django.test import TestCase, Client
from .models import Product, User
from .forms import ProductForm
from django.urls import reverse


#############################################################     
#############################################################  
# On INITIALISE NOTRE TEST AFIN DE VERIFIER SI LES DONNEES TEXTUELS SONT CORRECTS
class TestCaseProduct(TestCase):
  
  #TEST SI UN DONNEES est bien saisi
  #methode setUp se declenche a chaque fois qu'un test va débuter
  def setUp(self):
    self.product = Product.objects.create(
      title= "Produit 1",
      price = 15.15,
      description="Lorem ispum dolor sit amet",
      date_added= "2024-06-15",
      quantity=2
    )
    
  #on test si la fonction title est bien egal a un valeur attendu
  def test_product(self):
    self.assertEqual(self.product.title, "Produit 1")
    

#############################################################   
#############################################################  
#ON TESTE NOS FORMULAIRES
class TestCaseFormProduct(TestCase):
  
  def setUp(self):
    self.data = {
      "title": "Produit 1",
      "price" : 15.15,
      "description":"Lorem ispum dolor sit amet",
      "date_added": "2024-06-15",
      "quantity":2
    }
    self.product = Product.objects.create(**self.data)
          
  #On verifie si les données du formulaire 
  #d'ajout de produit fonctionne bien avec les données saisi
  def test_valid_form_product(self):
    form = ProductForm(self.data)
    self.assertTrue(form.is_valid()) 
    
    
    
#############################################################   
############################################################# 
#ON TEST NOS VUES
class TestCaseAuthenticationn(TestCase):
  def setUp(self):
    self.data_auth = {
      "username" : "test",
      "password1" : "test",
      "password2" : "test",
      "email" : "test@gmail.com"
    }
    
    self.user_connect = User.objects.create_user(self.data_auth)
    
     #On utilise un client pour tester le formulaire pour simuler les vues 
    #Comme si on était dans un navigateur
    
    #On instancie le client
    self.client = Client()
    
    
  def test_register_view(self):
    #On prend l'url pour s'inscrire avec revers
    
    #on insere l'url concernée
    url = reverse("creation_compte")
    
    #On appelle notre url pour y accéder
    response = self.client.get(url)
    
    #On verfie que le statut retournée est bien correct
    #200 pour dire que la correction est correct
    self.assertEqual(response.status_code, 200)
    
    #############################################################   
    ############################################################# 
    #ON ENVOI DES DONNEES SUR CETTE VUES
    send_data_client = {
      "username" : "usernameTest",
      "first_name" : "firstNameTest",
      "last_name" : "lastNameTest",
      "email" : "emailTest@gmail.com",
      "password1" : "testpassword123**",
      "password2" : "testpassword123**"
    }
    
    #On envoi les données 
    response_send_data = self.client.post(url, send_data_client)
    
    #On verfie que le statut retournée est bien correct    
    #302 pour dire que la creation d'un instance est correct
    self.assertEqual(response_send_data.status_code, 302)
    
    #On verifie si maintenant l'utliisateur existe en base
    self.assertTrue(User.objects.filter(username="usernameTest").exists())
    
    #On verifie si la redirection a bien lieu sur la page du comptte utilisateur pour valider la commande 
    # avec le code 200
    self.assertRedirects(
      response_send_data,
      expected_url=reverse("account_user"),
      status_code=302
    )
    
    

#############################################################   
############################################################# 
#ON TEST LE FORMULAIRE DE CONNEXION
class TestCaseLogin(TestCase):
  def setUp(self):
    self.data_auth = {
      "username" : "test",
      "password1" : "test",
      "password2" : "test",
      "email" : "test@gmail.com"
    }
    
    self.user_connect = User.objects.create_user(self.data_auth)
    
    #On utilise un client pour tester le formulaire pour simuler les vues 
    #Comme si on était dans un navigateur
    
    #On instancie le client
    self.client = Client()
    
    
  #On test le formulaire de login une fois que le user est créer
  def test_login_user(self):
    url_login = reverse("connexion_compte")
    
    response_to_login = self.client.get(url_login)
    
    #On verifie qu'on est bien dans l'url de connexion de compte (login)
    self.assertEqual(response_to_login.status_code, 200)
    
    
    #On entre nos donnees de connexion de compte (login)
    response_to_login = self.client.post({
      "username": "test",
      "password": "test"
    })
        
    #On verifie si iil est bien authentifie à son espace personnel
    self.assertTrue(self.user_connect.is_authenticated)
    
    
class TestCaseLogout(TestCase):
    def setUp(self):
      self.data_auth = {
        "username" : "test",
        "password1" : "test",
        "password2" : "test",
        "email" : "test@gmail.com"
      }
      
      self.user_connect = User.objects.create_user(self.data_auth)
      
      #On utilise un client pour tester le formulaire pour simuler les vues 
      #Comme si on était dans un navigateur
      
      #On instancie le client
      self.client = Client()
      
      
    #On test la déconnexion d'un user
    def test_logout_user(self):
      
      #On verfiie qu'un user est bien connecté
      self.client.login(username=self.data_auth['username'], password=self.data_auth['password1'])
      
      url_logout = reverse("logout")
      
      response_logout = self.client.get(url_logout)
      
      self.assertEqual(response_logout.status_code, 302)
      
      self.assertRedirects(response_logout, reverse("connexion_compte"), 302)
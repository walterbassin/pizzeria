

from django.shortcuts import render, redirect
from django.contrib.auth.forms import  AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.views.generic import UpdateView
from django.urls import reverse

# Create your views here.
from pizza_web.models import pizza, empanada, bebida, postre, portada, secundaria_portada, about_portada
from pizza_web.forms import pizza_form, empanada_form, bebida_form, postre_form, User_registration_form, User_edit_form, portada_form, portada_about_form, portada_secundaria_form 


# Create your views here.

def editar_usuario(request):
    usuario=request.user
    if request.method == 'POST':
        form = User_edit_form (request.POST, request.FILES)
        if form.is_valid():
                usuario.email=form.cleaned_data['email']
                usuario.first_name=form.cleaned_data ['first_name']        
                usuario.last_name=form.cleaned_data ['last_name']
                usuario.description=form.cleaned_data ['description']
                usuario.link=form.cleaned_data ['link']
                usuario.password1=form.cleaned_data ['password1']
                usuario.password2=form.cleaned_data ['password1']
                usuario_validar = form.cleaned_data['image']
                if usuario_validar is not None:
                    usuario.image = form.cleaned_data ['image']     
                usuario.save()
                context = {'usuario': usuario}
                return render (request, 'perfil_usuario.html', context = context)
        else:
            errors=form.errors
            form=User_edit_form()
            context={'errors': errors, 'form': form}
            return render(request, 'update_user.html', context=context)
        
    else:
        form = User_edit_form (initial={ 'first_name': usuario.first_name, 'last_name':usuario.last_name,'email': usuario.email, 'description': usuario.description, 'link': usuario.link})
        context={'form': form}
        return render(request, 'update_user.html', context=context)

def perfil_usuario_view (request):
    usuario=request.user
    context = {'usuario': usuario}
    return render(request, 'perfil_usuario.html', context=context)

class update_pizza(UpdateView):
    model= pizza
    template_name = 'update_pizza.html'
    fields = '__all__'

    def get_success_url (self):
        return reverse('pizza_detail', kwargs={'pk' : self.object.pk})

class update_empanada(UpdateView):
    model= empanada
    template_name = 'update_empanada.html'
    fields = '__all__'

    def get_success_url (self):
        return reverse('empanada_detail', kwargs={'pk' : self.object.pk})

class update_bebida(UpdateView):
    model= bebida
    template_name = 'update_bebida.html'
    fields = '__all__'

    def get_success_url (self):
        return reverse('bebida_detail', kwargs={'pk' : self.object.pk})

class update_postre(UpdateView):
    model= postre
    template_name = 'update_postre.html'
    fields = '__all__'

    def get_success_url (self):
        return reverse('postre_detail', kwargs={'pk' : self.object.pk})

def login_view(request):
    if  request.method== 'POST':
        form = AuthenticationForm(request, data = request.POST)

        if form.is_valid():
            username=form.cleaned_data['username']
            password = form.cleaned_data ['password']
            user = authenticate(username=username, password = password)

            if user is not None:
                login(request, user)
                portadas = portada.objects.get(id=1)
                portadas_secundarias = secundaria_portada.objects.get(id=1)
                portadas_about = about_portada.objects.get(id=1)
                context={'portadas': portadas, 'portadas_secundarias': portadas_secundarias, 'portadas_about': portadas_about}
                return  render(request, 'index.html', context = context)
            else:
                context= {'error':"No hay ningún usuario con esas credenciales"}
                form=AuthenticationForm()
                return render(request, 'login.html', context=context)
        else:
            errors=form.errors
            form=AuthenticationForm()
            context={'errors': errors, 'form': form}
        return render(request, 'login.html', context=context)  

    else:
        form = AuthenticationForm()
        context= {'form': form}
        return render(request, 'login.html', context=context)

def register_view(request):
    if request.method == 'POST':
        form=User_registration_form(request.POST, request.FILES)
        
        if form.is_valid():
            form.save()
            username =form.cleaned_data['username']
            password=form.cleaned_data['password1']
            user = authenticate(username = username, password = password)
            login(request, user)
            portadas = portada.objects.get(id=1)
            portadas_secundarias = secundaria_portada.objects.get(id=1)
            portadas_about = about_portada.objects.get(id=1)
            context={'portadas': portadas, 'portadas_secundarias': portadas_secundarias, 'portadas_about': portadas_about}
            return render (request, 'index.html', context = context)
        else:
            errors=form.errors
            form=User_registration_form()
            context={'errors': errors, 'form': form}
            return render(request, 'register.html', context=context)
    else:
        form = User_registration_form()
        context = {'form': form}
        return render (request, 'register.html', context = context)

def logout_view (request):
    logout(request)
    return redirect ('index')

def elements_view(request):
    pizzas= pizza.objects.all()
    empanadas= empanada.objects.all()
    bebidas= bebida.objects.all()
    postres= postre.objects.all()
    context ={'pizzas':pizzas, 'empanadas':empanadas, 'bebidas': bebidas, 'postres':postres}
    return render (request, 'elements.html', context=context)


def pizza_view (request):
    pizzas= pizza.objects.all()
    context={'pizzas': pizzas}
    return render (request, 'pizzas.html', context=context)


def pizza_detail_view(request, pk):
    if request.user.is_authenticated:
        pizza_detalle = pizza.objects.get(id=pk)
        context = {'pizza_detalle' : pizza_detalle}
        return render (request, 'pizza_detail.html', context = context)
    else:
        return redirect ('login')

def eliminar_pizza_view(request, pk):
    pizza_eliminada=pizza.objects.get(id=pk)
    if request.method ==  'GET':
        context = {'pizza_eliminada': pizza_eliminada}
    else:
        pizza_eliminada.delete()
        return redirect ('pizzas')
    
    return render(request, 'eliminar_pizza.html', context=context)


def empanada_view (request):
    empanadas= empanada.objects.all()
    context={'empanadas': empanadas}
    return render (request, 'empanadas.html', context=context)

def eliminar_empanada_view(request, pk):
    empanada_eliminada=empanada.objects.get(id=pk)
    if request.method ==  'GET':
        context = {'empanada_eliminada': empanada_eliminada}
    else:
        empanada_eliminada.delete()
        return redirect ('empanadas')
    
    return render(request, 'eliminar_empanada.html', context=context)

def empanada_detail_view (request, pk):
    if request.user.is_authenticated:
        empanada_detalle=empanada.objects.get (id=pk)
        context = {'empanada_detalle': empanada_detalle}
        return render(request, 'empanada_detail.html', context = context)
    else:
        return redirect ('login')

def bebida_view (request):
    bebidas= bebida.objects.all()
    context={'bebidas': bebidas}
    return render (request, 'bebidas.html', context=context)

def eliminar_bebida_view(request, pk):
    bebida_eliminada=bebida.objects.get(id=pk)
    if request.method ==  'GET':
        context = {'bebida_eliminada': bebida_eliminada}
    else:
        bebida_eliminada.delete()
        return redirect ('bebidas')
    
    return render(request, 'eliminar_bebida.html', context=context)

def bebida_detail_view (request, pk):
    if request.user.is_authenticated:
        bebida_detalle=bebida.objects.get (id=pk)
        context = {'bebida_detalle': bebida_detalle}
        return render(request, 'bebida_detail.html', context = context)
    else:
        return redirect ('login')

def postre_view (request):
    postres= postre.objects.all()
    context={'postres': postres}
    return render (request, 'postres.html', context=context)

def eliminar_postre_view(request, pk):
    postre_eliminado=postre.objects.get(id=pk)
    if request.method ==  'GET':
        context = {'postre_eliminado': postre_eliminado}
    else:
        postre_eliminado.delete()
        return redirect ('postres')
    
    return render(request, 'eliminar_postre.html', context=context)

def postre_detail_view (request, pk):
    if request.user.is_authenticated:
        postre_detalle=postre.objects.get (id=pk)
        context = {'postre_detalle': postre_detalle}
        return render(request, 'postre_detail.html', context = context)
    else:
        return redirect ('login')

def index_view (request):
    portadas = portada.objects.get(id=1)
    portadas_secundarias = secundaria_portada.objects.get(id=1)
    portadas_about = about_portada.objects.get(id=1)
    context={'portadas': portadas, 'portadas_secundarias': portadas_secundarias, 'portadas_about': portadas_about}
    return render (request, 'index.html', context=context)

class update_portada_view(UpdateView):
    model= portada
    template_name = 'update_portada.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse('index')

class update_portada_secundaria__view(UpdateView):
    model= secundaria_portada
    template_name = 'update_portada_secundaria.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse('index')


def about_view (request):
    portadas_about = about_portada.objects.get(id=1)
    context={'portadas_about': portadas_about}
    return render (request, 'about.html', context=context)

def agregar_pizza_view (request):
  if request.user.is_authenticated and request.user.is_superuser:
    if request.method == 'GET':
        form = pizza_form()
        context = {'form':form}
        return render(request, 'agregar_pizza.html', context=context)
    else:
        form = pizza_form(request.POST, request.FILES)
        if form.is_valid():
            new_pizza= pizza.objects.create(
                nombre = form.cleaned_data['nombre'],
                precio = form.cleaned_data['precio'],
                ingredientes = form.cleaned_data['ingredientes'],
                apto_delivery = form.cleaned_data['apto_delivery'],
                vegana = form.cleaned_data['vegana'],
                foto=form.cleaned_data['foto']
            )
            context ={'new_pizza':new_pizza}
        else:
            context = {'errors': form.errors}
        return render(request, 'agregar_pizza.html', context=context)
  else:
      return redirect('login')

def agregar_empanada_view (request):
 if request.user.is_authenticated and request.user.is_superuser:
    if request.method == 'GET':
        form = empanada_form()
        context = {'form':form}
        return render(request, 'agregar_empanada.html', context=context)
    else:
        form = empanada_form(request.POST, request.FILES)
        if form.is_valid():
            new_empanada= empanada.objects.create(
                nombre = form.cleaned_data['nombre'],
                precio = form.cleaned_data['precio'],
                ingredientes = form.cleaned_data['ingredientes'],
                apto_delivery = form.cleaned_data['apto_delivery'],
                foto=form.cleaned_data['foto'],
            )
            context ={'new_empanada':new_empanada}
        else:
            context = {'errors': form.errors}        
        return render(request, 'agregar_empanada.html', context=context)
 else:
     return redirect ('login')

def agregar_bebida_view (request):
 if request.user.is_authenticated and request.user.is_superuser:
    if request.method == 'GET':
        form = bebida_form()
        context = {'form':form}
        return render(request, 'agregar_bebida.html', context=context)
    else:
        form = bebida_form(request.POST, request.FILES)
        if form.is_valid():
            new_bebida= bebida.objects.create(
                nombre = form.cleaned_data['nombre'],
                precio = form.cleaned_data['precio'],
                apto_delivery = form.cleaned_data['apto_delivery'],
                foto=form.cleaned_data['foto'],
            )
            context ={'new_bebida':new_bebida}
        else:
            context = {'errors': form.errors}
        return render(request, 'agregar_bebida.html', context=context)
 else:
     return redirect ('login')


def agregar_postre_view (request):
 if request.user.is_authenticated and request.user.is_superuser:
    if request.method == 'GET':
        form = postre_form()
        context = {'form':form}
        return render(request, 'agregar_postre.html', context=context)
    else:
        form = postre_form(request.POST, request.FILES)
        if form.is_valid():
            new_postre= postre.objects.create(
                nombre = form.cleaned_data['nombre'],
                precio = form.cleaned_data['precio'],
                apto_delivery = form.cleaned_data['apto_delivery'],
                gluten_free  =form.cleaned_data ['gluten_free'],
                foto=form.cleaned_data['foto']
            )
            context ={'new_postre':new_postre}
        else:
            context = {'errors': form.errors}
        return render(request, 'agregar_postre.html', context=context)
 else:
     return redirect ('login')

def buscar_view(request):
    producto_busqueda = request.GET['search']
    buscar_pizza = pizza.objects.filter(nombre__icontains = producto_busqueda)
    buscar_empanada = empanada.objects.filter(nombre__icontains = producto_busqueda)
    buscar_bebida = bebida.objects.filter(nombre__icontains = producto_busqueda)
    buscar_postre= postre.objects.filter(nombre__icontains = producto_busqueda)
    
    if buscar_pizza.exists() or buscar_empanada.exists() or buscar_bebida.exists() or buscar_postre.exists():
        context = {'buscar_pizza':buscar_pizza, 'buscar_empanada': buscar_empanada, 'buscar_bebida': buscar_bebida, 'buscar_postre': buscar_postre}
    elif producto_busqueda == 'pizza' or producto_busqueda=='pizzas':
        buscar_pizza=pizza.objects.all()
        context = {'buscar_pizza':buscar_pizza}
    elif producto_busqueda == 'empanada' or producto_busqueda=='empanadas':
        buscar_empanada=empanada.objects.all()
        context = {'buscar_empanada':buscar_empanada}
    elif producto_busqueda == 'bebida' or producto_busqueda=='bebidas':
        buscar_bebida=bebida.objects.all()
        context = {'buscar_bebida':buscar_bebida}
    elif producto_busqueda == 'postre' or producto_busqueda=='postres':
        buscar_postre=postre.objects.all()
        context = {'buscar_postre':buscar_postre}
    else:
        context= {'errors': f"Disculpe, no encontramos un producto con el texto {producto_busqueda}."}
    return render(request, 'buscar.html', context = context)

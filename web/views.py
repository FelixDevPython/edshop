from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Los decoradores son funciones que se utilizan para modificar el comportamiento de una función
# El decorador login_required lo que va a hecer es antes de ejecutar la funcion, va a verificar si el usuario esta logueado dejando entrar a la funcion pero si no lo esta, lo redirige a la pagina de login
from .models import Categoria,Producto,Cliente
from .carrito import Cart
from .forms import ClienteForm

# Create your views here.
""" VISTAS PARA MOSTRAR EL CATALOGO DE PRODUCTOS """

def index(request):
    listaProductos = Producto.objects.all()
    listaCategorias = Categoria.objects.all()
    #print(listaProductos)
    context = {
        'categorias': listaCategorias,
        'productos': listaProductos,
    }
    return render(request, 'index.html',context)

def productosPorCategoria(request, categoria_id):
    """ vista para filtrar productos por categoria """
    objCategoria = Categoria.objects.get(pk=categoria_id)
    listaProductos = objCategoria.producto_set.all()
    listaCategorias = Categoria.objects.all()

    context = {       
        'categorias': listaCategorias,
        'productos': listaProductos,
    }

    return render(request, 'index.html',context)

def productosPorNombre(request):
    """ vista para filtrado de productos por nombre """
    nombre = request.POST['nombre']
    listaProductos = Producto.objects.filter(nombre__contains=nombre)
    listaCategorias = Categoria.objects.all()

    context = {       
        'categorias': listaCategorias,
        'productos': listaProductos,
    }

    return render(request, 'index.html',context)

def productoDetalle(request, producto_id):
    """ vista para mostrar el detalle de un producto """
    #objProducto = Producto.objects.get(pk=producto_id)
    objProducto = get_object_or_404(Producto, pk=producto_id)    
    context = {
        'producto': objProducto,
    }

    return render(request, 'producto.html',context)

""" vistas para el carrito de compras """
def carrito(request):
    return render(request, 'carrito.html')

def agregarCarrito(request, producto_id):
    if request.method == 'POST':
        cantidad = int(request.POST['cantidad'])
    else:
        cantidad = 1

    objProducto = Producto.objects.get(pk=producto_id)
    carritoProducto = Cart(request)
    carritoProducto.add(objProducto, cantidad)

    #print(request.session.get('cart'))

    if request.method == 'GET':
        return redirect('/')

    return render(request, 'carrito.html')

def eliminarProductoCarrito(request, producto_id):
    objProducto = Producto.objects.get(pk=producto_id)
    carritoProducto = Cart(request)
    carritoProducto.delete(objProducto)

    return render(request, 'carrito.html')

def limpiarCarrito(request):
    carritoProducto = Cart(request)
    carritoProducto.clear()
    return render(request, 'carrito.html')


""" VISTAS PARA CLIENTES Y USUARIOS """
def crearUsuario(request):

    if request.method == 'POST':
        dataUsuario = request.POST['nuevoUsuario']
        dataPassword = request.POST['nuevoPassword']

        nuevoUsuario = User.objects.create_user(username=dataUsuario, password=dataPassword)
        if nuevoUsuario is not None:
            login(request, nuevoUsuario)
            return redirect('/cuenta')

    return render(request, 'login.html')

def loginUsuario(request):
    paginaDestino = request.GET.get('next')
    # Se obtiene la pagina a la que se quiere redirigir al usuario una vez logueado
    context = {
        'destino': paginaDestino,
    }

    if request.method == 'POST':
        dataUsuario = request.POST['usuario']
        dataPassword = request.POST['password']
        dataDestino = request.POST['destino']
        # Se obtiene el destino al que se quiere redirigir al usuario una vez logueado

        usuarioAuth = authenticate(request,username=dataUsuario, password=dataPassword)
        if usuarioAuth is not None:
            login(request, usuarioAuth)

            if dataDestino != 'None':
                # Si el destino no es None, se redirige a la pagina destino
                return redirect(dataDestino)

            return redirect('/cuenta')
        else:
            context = {
                'mensajeError':'Datos incorrectos',
            }

    return render(request, 'login.html', context)

def logoutUsuario(request):
    logout(request)
    return render(request,'login.html')

def cuentaUsuario(request):
    try:
        clienteEditar = Cliente.objects.get(usuario=request.user)
        # Se obtiene el usuario que se logueo, como parametro a la variable usuario y va a obtener el cliente
        dataCliente = {
            # Estos datos vienen del usuario que se logueo, que esta dentro de la variable request, que se crea al loguearse
            # Estos datos vienen de la tabla usuario
            'nombre':request.user.first_name,
            'apellidos':request.user.last_name,
            'email':request.user.email,
            # Estos datos vienen de la tabla cliente
            'direccion':clienteEditar.direccion,
            'telefono':clienteEditar.telefono,
            'dni':clienteEditar.dni,
            'sexo':clienteEditar.sexo,
            'fecha_nacimiento':clienteEditar.fecha_nacimiento,
        }
    except:
        dataCliente = {
            'nombre':request.user.first_name,
            'apellidos':request.user.last_name,
            'email':request.user.email,
        }
        # Si no existe el cliente, se crea un diccionario con los datos del usuario logueado, los datos vienen desde la tabla usuario

    frmCliente = ClienteForm(dataCliente)
    # Se crea una instancia del formulario ClienteForm, y se le pasa el diccionario dataCliente
    context = {
        'frmCliente': frmCliente,
    }

    return render(request, 'cuenta.html', context)

def actualizarCliente(request):
    mensaje = ""
    if request.method == 'POST':
        frmCliente = ClienteForm(request.POST)
        # Todo lo que se envie por POST se va a signar a la clase ClienteForm
        if frmCliente.is_valid():
            # El metodo is_valid() valida los datos
            dataCliente = frmCliente.cleaned_data
            # El metodo cleaned_data prepara la data para ser guardada en la base de datos
            actUsuario = User.objects.get(pk=request.user.id)
            # Se obtiene el usuario que se va a actualizar, en este caso el que esta logeado
            actUsuario.first_name = dataCliente['nombre']
            actUsuario.last_name = dataCliente['apellidos']
            actUsuario.email = dataCliente['email']
            actUsuario.save()
            
            # Registrar Cliente
            nuevoCliente = Cliente()
            nuevoCliente.usuario = actUsuario
            nuevoCliente.dni = dataCliente['dni']
            nuevoCliente.direccion = dataCliente['direccion']
            nuevoCliente.telefono = dataCliente['telefono']
            nuevoCliente.sexo = dataCliente['sexo']
            nuevoCliente.fecha_nacimiento = dataCliente['fecha_nacimiento']
            nuevoCliente.save()

            mensaje = "Datos actualizados"

    context = {
        'mensaje': mensaje,
        'frmCliente': frmCliente,
    }

    return render(request, 'cuenta.html', context)

""" VISTAS PARA PROCESO DE COMPRA """
@login_required(login_url='/login')
def registrarPedido(request):
    try:
        clienteEditar = Cliente.objects.get(usuario=request.user)
        dataCliente = {
            'nombre':request.user.first_name,
            'apellidos':request.user.last_name,
            'email':request.user.email,
            'direccion':clienteEditar.direccion,
            'telefono':clienteEditar.telefono,
            'dni':clienteEditar.dni,
            'sexo':clienteEditar.sexo,
            'fecha_nacimiento':clienteEditar.fecha_nacimiento,
            }
    except:
        dataCliente = {
            'nombre':request.user.first_name,
            'apellidos':request.user.last_name,
            'email':request.user.email,
        }

    frmCliente = ClienteForm(dataCliente)
    context = {
        'frmCliente': frmCliente,
    }

    return render(request, 'pedido.html', context)



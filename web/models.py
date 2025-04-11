from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Categoria(models.Model):
    nombre = models.CharField(max_length=200)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre
    
class Producto(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.RESTRICT)
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(null=True)
    precio = models.DecimalField(max_digits=9, decimal_places=2)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    imagen = models.ImageField(upload_to='productos', blank=True)

    def __str__(self):
        return self.nombre
    
class Cliente(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.RESTRICT)
    dni= models.CharField(max_length=8)
    sexo = models.CharField(max_length=1, default='M')
    telefono = models.CharField(max_length=20)
    fecha_nacimiento = models.DateField(null=True)
    direccion = models.TextField()

    def __str__(self):
        return self.dni
    
class Pedido(models.Model):

    ESTADO_CHOICES = (
        ('0', 'Solicitado'),
        ('1', 'Pagado'),
    )

    cliente = models.ForeignKey(Cliente, on_delete=models.RESTRICT)
    # RESTRICT: No se puede eliminar un cliente si tiene pedidos
    fecha_registro = models.DateTimeField(auto_now_add=True)
    nro_pedido = models.CharField(max_length=20, null=True)
    monto_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estado = models.CharField(max_length=20, default='0', choices=ESTADO_CHOICES)
    # 0: Solicitado, 1: Pagado

    def __str__(self):
        return self.nro_pedido
    
class PedidoDetalle(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.RESTRICT)
    producto = models.ForeignKey(Producto, on_delete=models.RESTRICT)
    cantidad = models.IntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    # Se usa subtotal porque el precio puede cambiar, en caso de que no almacenaras el costo que tuvo el producto al momento de la venta, cuando se cambie el precio, se va a perder ese dato, de esta manera se registra a cuanto se vendió el producto, si quiero saber el precio unitario en el momento de la venta, lo puedo obtener dividiendo el subtotal entre la cantidad
    def __str__(self):
        return self.producto.nombre
    

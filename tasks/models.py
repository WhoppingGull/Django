from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

# Modelo para Usuarios
class Usuario(AbstractUser):
    ROL_CHOICES = [
        ('superadministrador', 'Superadministrador'),
        ('administrador', 'Administrador'),
        ('usuario ordinario', 'Usuario Ordinario'),
    ]
    rol = models.CharField(max_length=20, choices=ROL_CHOICES)
    activo = models.BooleanField(default=True)
    
    # Ajuste de los nombres relacionados para evitar conflictos
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',  # Cambio de nombre relacionado
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions_set',  # Cambio de nombre relacionado
        blank=True,
    )

    def __str__(self):
        return self.username

#ECHO
# Modelo para Productos
class Producto(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    creacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre
#ECHO
# Modelo para Empleados
class Empleado(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    puesto = models.CharField(max_length=100)
    creacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.nombre} {self.apellido}'


#echo
# Modelo para Clientes
class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    creacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.nombre} {self.apellido}'

#ECHO
# Modelo para Proveedores
class Proveedor(models.Model):
    nombre = models.CharField(max_length=255)
    contacto = models.CharField(max_length=255, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    creacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


# Modelo para Ventas
class Venta(models.Model):
    fecha = models.DateField()
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    creacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f'Venta {self.id}'

class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    iva = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    creacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f'Detalle {self.id} de Venta {self.venta.id}'

    def toJSON(self):
        item = model_to_dict(self, exclude=['creacion'])
        return item

# Modelo para Compras
class Compra(models.Model):
    fecha = models.DateField()
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    creacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f'Compra {self.id}'

# Modelo para Detalles de Compra
class DetalleCompra(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    creacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f'Detalle {self.id} de Compra {self.compra.id}'

# Modelo para Maquinaria
class Maquinaria(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    ubicacion = models.CharField(max_length=255, blank=True, null=True)
    creacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

# Modelo intermedio para Proveedores y Productos
class ProveedorProducto(models.Model):
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    creacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    class Meta:
        unique_together = ('proveedor', 'producto')

    def __str__(self):
        return f'{self.proveedor.nombre} suministra {self.producto.nombre}'

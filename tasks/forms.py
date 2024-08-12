from django.forms import ModelForm
from .models import Producto, Empleado, Cliente, Proveedor,Venta,DetalleVenta
from django import forms

class empleadotoforms(ModelForm):
    class Meta:
        model = Empleado
        fields = ['nombre','apellido','email','telefono','direccion','puesto']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del empleado'
            }),
            'apellido': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Apellido del empleado'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email del empleado'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Teléfono del empleado'
            }),
            'direccion': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Dirección del empleado',
                'rows': 3
            }),
            'puesto': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Puesto del empleado'
            }),
        }

class productoforms(ModelForm):
   class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'stock']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del producto'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Descripción del producto',
                'rows': 3
            }),
            'precio': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Precio del producto'
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Cantidad en stock'
            }),
        }


class clienteforms(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido', 'email', 'telefono', 'direccion']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del cliente'
            }),
            'apellido': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Apellido del cliente'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Correo electrónico del cliente'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de teléfono del cliente'
            }),
            'direccion': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Dirección del cliente',
                'rows': 3
            }),
        }

class proveedorforms(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nombre', 'contacto', 'telefono', 'direccion']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la distribuidora'
            }),
            'contacto': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del porveedor'
            }),
            
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de teléfono del porveedor',
                'type': 'tel'
            }),
            'direccion': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Dirección del porveedor',
                'rows': 3
            }),
        }
        
class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['fecha', 'cliente']
        widgets = {
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'cliente': forms.Select(attrs={'class': 'form-control'}),
        }

class DetalleVentaForm(forms.ModelForm):
    cantidad = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 1}))
    
    class Meta:
        model = DetalleVenta
        fields = ['producto', 'cantidad']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-control'}),
        }

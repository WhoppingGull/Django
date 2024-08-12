from django.http import HttpResponse
from django.utils.timezone import now
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.forms import formset_factory
from .forms import productoforms,empleadotoforms,clienteforms,proveedorforms,VentaForm,DetalleVentaForm

from .models import Producto,Empleado,Cliente,Proveedor,Venta,DetalleVenta
from django.shortcuts import render, get_object_or_404, redirect
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from django.core.files.base import ContentFile
from PIL import Image
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
import datetime
from xhtml2pdf import pisa
import os
import tempfile
from io import BytesIO
import base64
from django.db import models
from django.template.loader import get_template
#from weasyprint import HTML, CSS
from decimal import Decimal
from django.views.generic import View
from django.conf import settings
from django.forms import formset_factory
# Create your views here.
def home(request):
    return render(request, 'home.html')

# Función para mandar a llenar el formulario de signup
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            try:
                user=form.save()
                # form.save()  Esto guarda el nuevo usuario en la base de datos
                login(request,user) # Inicia sesión al usuario recién creado
                return redirect('tasks')  # Redirige al apartado de 'task'
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': form,
                    'error': 'Uusario existe en la base de datos.'
                })
        else:
            return render(request, 'signup.html', {
                'form': form,
                'error': 'Las contraseñas no coinciden o hay otros errores.'
            })
    else:
        form = UserCreationForm()
        return render(request, 'signup.html', {
            'form': form
        })
        

#cierra cecison 
def logoutt(request):
    logout(request)
    return redirect('home')
    

def signin(request):
    if request.method =='GET':
        return render(request, 'signin.html',{
            'form': AuthenticationForm()
        })
    else:
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)  # Inicia sesión al usuario
            return redirect('tasks')  # Redirige al apartado de 'tasks'
        else:
            
            return render(request, 'signin.html', {
                'form': form,
                'error': 'Usuario o contraseña incorrecta'
            })




#Crea un Empleado
def crear_empleado(request):
    if request.method == 'GET':
        return render(request, 'crear_empleado.html',{
            'form': empleadotoforms
        })
    else:
       try:
           form = empleadotoforms(request.POST)
           nuevo_emp = form.save(commit=False)
           nuevo_emp.save()
           return redirect('tasks')
       except ValueError:
           return render(request, 'crear_empleado.html',{
            'form': empleadotoforms,
            'error': 'Por favor ingrese datos validos en el sistema'
        })    
        
#Crea producto
def crear_producto(request):
    if request.method == 'GET':
        return render(request, 'crear_producto.html',{
            'form': productoforms
        })
    else:
       try:
           form = productoforms(request.POST)
           nuevo_producto = form.save(commit=False)
           nuevo_producto.save()
           return redirect('tasks')
       except ValueError:
           return render(request, 'crear_producto.html',{
            'form': productoforms,
            'error': 'Por favor ingrese datos validos en el sistema'
        })

#Crear Cliente
def crear_clientes(request):
    if request.method== 'GET':
        return render(request, 'crear_clientes.html',{
                      'form' : clienteforms})
    else:
        try:
           form = clienteforms(request.POST)
           nuevo_cli = form.save(commit=False)
           nuevo_cli.save()
           return redirect('clientes')
        except ValueError:
           return render(request, 'crear_clientes.html',{
            'form': clienteforms,
            'error': 'Por favor ingrese datos validos en el sistema'
        })

#Crear proveedor
def crear_proveedor(request):
    if request.method=='GET':
        return render(request,'crear_proveedor.html',{
            'form' : proveedorforms
        })
    else:
        try:
            form = proveedorforms(request.POST)
            nuevo_pro = form.save(commit=False)
            nuevo_pro.save()
            return redirect('proveedor')
        except ValueError:
            return render(request,'crear_proveedor.html',{
                'form': proveedorforms,
                'error': 'Por favor ingrese datos validos en el sistema'
            })


def calcular_total(detalle_forms):
    total = 0
    for form in detalle_forms:
        if form.cleaned_data:
            producto = form.cleaned_data['producto']
            cantidad = form.cleaned_data['cantidad']
            if producto and cantidad:
                precio_unitario = producto.precio
                total += cantidad * precio_unitario
    return total

#Crear venta
def crear_venta(request):
    if request.method == 'POST':
        venta_form = VentaForm(request.POST)
        DetalleVentaFormSet = formset_factory(DetalleVentaForm, extra=1)
        detalle_formset = DetalleVentaFormSet(request.POST)
        
        if venta_form.is_valid() and detalle_formset.is_valid():
            venta = venta_form.save(commit=False)
            venta.save()
            
            total_venta = calcular_total(detalle_formset)
            print(total_venta)
    
            

#Enlisats clientes
def clientes(request):
    cliente=Cliente.objects.filter(activo=True)
    return render(request, 'clientes.html',{
        'cliente' : cliente
    })

#Enlista los empleados
def empleados(request):
    empleados=Empleado.objects.filter(activo=True)
    return render(request, 'empleados.html',{
        'empleados' : empleados
    })

#Enlista el producto
def tasks(request):
    productos = Producto.objects.filter(activo=True)
    print(productos)
    return render(request, 'tasks.html', {
        'productos': productos})

#Enlistar Proveedor
def proveedor(request):
    proveedor = Proveedor.objects.filter(activo=True)
    return render(request,'proveedor.html',{
        'proveedor':proveedor
    })

#Enlisatra venta 
def venta(request):
    venta=Venta.objects.filter(activo=True)
    return render(request,'venta.html',{
        'venta':venta
    })

#Elimina Empleados
def eliminar_empleado(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)
    if request.method == 'POST':
        empleado.activo = False
        empleado.save()
        return redirect('empleados')
    return render(request, 'confirmar_eliminacionEmp.html', {'empleado': empleado})

#Elimna producto
def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.activo = False
        producto.save()
        return redirect('tasks')
    return render(request, 'confirmar_eliminacion.html', {'producto': producto})

#Elimar cliente
def eliminar_clientes(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if reques.method == 'POST':
        cliente.activo=False
        cliente.save()
        return redirect('clientes')
    return render(request,'confirmar_eliminacionCli.html',{
        'cliente':cliente
    })

#Elimianr Proveedor
def eliminar_proveedor(request,pk):
    proveedor = get_object_or_404(Proveedor,pk=pk)
    if request.method == 'POST':
        proveedor.activo=False
        proveedor.save()
        return redirect('proveedor')
    return render(request, 'confirmar_eliminacionPro.html',{
        'proveedor':proveedor
    })
        
        



#Ediar cliente
def editar_clientes(request,pk):
    cliente=get_object_or_404(Cliente,pk=pk)
    if request.method == 'POST':
        form=clienteforms(request.POST,instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('clientes')
    else:
        form = clienteforms(instance=cliente)
    return render(request, 'editar_clientes.html', {'form': form, 'cliente': cliente})
    
#Editar Empleado
def editar_empleado(request,pk):
    empleado = get_object_or_404(Empleado, pk=pk)
    if request.method == 'POST':
        form = empleadotoforms(request.POST, instance=empleado)
        if form.is_valid():
            form.save()
            return redirect('empleados')
    else:
        form = empleadotoforms(instance=empleado)
    return render(request, 'editar_empleado.html', {'form': form, 'empleado': empleado})

#Edita product
def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = productoforms(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('tasks')
    else:
        form = productoforms(instance=producto)
    return render(request, 'editar_producto.html', {
        'form': form, 'producto': producto})

#Ediastar Proveedor
def editar_proveedor(request,pk):
    proveedor = get_object_or_404(Proveedor,pk=pk)
    if request.method == 'POST':
        form = proveedorforms(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            return redirect('proveedor')
    else:
        form = proveedorforms(instance=proveedor)
    return render(request, 'editar_proveedor.html', {
        'form': form, 'proveedor': proveedor})



#Visualizar clinetes 
def ver_clientes(request,pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    form = empleadotoforms(instance=cliente)
    
    # Bloquear campos en el formulario
    for field in form.fields:
        form.fields[field].widget.attrs['disabled'] = 'disabled'
    
    return render(request, 'ver_cliente.html', {'form': form, 'cliente': cliente})

#Visaulizar Empleado
def ver_empleado(request,pk):
    empleado = get_object_or_404(Empleado, pk=pk)
    form = empleadotoforms(instance=empleado)
    
    # Bloquear campos en el formulario
    for field in form.fields:
        form.fields[field].widget.attrs['disabled'] = 'disabled'
    
    return render(request, 'ver_empleado.html', {'form': form, 'empleado': empleado})

#Visualizar productos
def ver_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    form = productoforms(instance=producto)
    
    # Bloquear campos en el formulario
    for field in form.fields:
        form.fields[field].widget.attrs['disabled'] = 'disabled'
    
    return render(request, 'ver_producto.html', {'form': form, 'producto': producto})

#Visaulizar proveedor
def ver_proveedor(request,pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    form = proveedorforms(instance=proveedor)
    
    # Bloquear campos en el formulario
    for field in form.fields:
        form.fields[field].widget.attrs['disabled'] = 'disabled'
    
    return render(request, 'ver_proveedor.html', {'form': form, 'proveedor': proveedor})




#Grafica de clinetes
def generar_grafica_clientes():
    # Obtener datos
    clientes = Cliente.objects.all()
    fechas = [cliente.creacion.date().strftime('%Y-%m') for cliente in clientes]
    
    # Contar clientes por mes
    fechas_unicas = sorted(set(fechas))
    conteo_clientes = [fechas.count(fecha) for fecha in fechas_unicas]
    
    # Crear la gráfica
    plt.figure(figsize=(10, 6))
    plt.bar(fechas_unicas, conteo_clientes, color='teal')
    plt.xlabel('Fecha de Creación')
    plt.ylabel('Número de Clientes')
    plt.title('Número de Clientes por Mes')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Guardar la gráfica en un buffer
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    return buffer

#Genera garfica de productos
def grafica_pastel():
    fig, ax = plt.subplots()
    productos = Producto.objects.all()
    nombres = [p.nombre for p in productos]
    precios = [p.precio for p in productos]
    
    # Crear una gráfica de pastel
    ax.pie(precios, labels=nombres, autopct='%1.1f%%', startangle=140)

    # Asegurar que el gráfico sea un círculo
    ax.axis('equal')
    

     # Guardar en un buffer en memoria
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    
    return buffer

#Genera garfica de productos
def generar_grafica():
    fig, ax = plt.subplots()
    productos = Producto.objects.filter(activo=True)
    nombres = [p.nombre for p in productos]
    precios = [p.precio for p in productos]

    ax.bar(nombres, precios)
    ax.set_xlabel('Producto')
    ax.set_ylabel('Precio')
    ax.set_title('Precios de Productos')

    # Guardar en un buffer en memoria
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    return buffer

#Genera Grafica de Empleados
def generar_grafica_Emp():
    # Contar empleados activos e inactivos
    activos = Empleado.objects.filter(activo=True).count()
    inactivos = Empleado.objects.filter(activo=False).count()

    # Datos para el gráfico
    labels = 'Activos', 'Inactivos'
    sizes = [activos, inactivos]
    colors = ['#4CAF50', '#FFC107']
    explode = (0.1, 0)  # Explode the 1st slice

    # Crear gráfico de pastel
    buffer = BytesIO()
    plt.figure(figsize=(8, 8))
    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
    plt.title('Proporción de Empleados Activos e Inactivos')
    plt.axis('equal')
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    return buffer

#Grafica proveedor
def generar_grafica_proveedores():
    # Obtener datos
    proveedores = Proveedor.objects.all()
    fechas = [proveedor.creacion.date().strftime('%Y-%m') for proveedor in proveedores]
    
    # Contar proveedores por mes
    fechas_unicas = sorted(set(fechas))
    conteo_proveedores = [fechas.count(fecha) for fecha in fechas_unicas]
    
    # Crear la gráfica
    plt.figure(figsize=(10, 6))
    plt.bar(fechas_unicas, conteo_proveedores, color='teal')
    plt.xlabel('Fecha de Creación')
    plt.ylabel('Número de Proveedores')
    plt.title('Número de Proveedores por Mes')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Guardar la gráfica en un buffer
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    return buffer


#genera infromes de Empleados
def generar_informe_empleados(request):
    empleados = Empleado.objects.all()
    fecha_actual = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    grafica_buffer = generar_grafica_Emp()
    
    total_empleados = empleados.count()
    empleados_activos = empleados.filter(activo=True).count()
    empleados_inactivos = empleados.filter(activo=False).count()

    # Guardar la gráfica en un archivo temporal
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
    temp_file.write(grafica_buffer.getvalue())
    temp_file.close()

    # Usa la ruta relativa del archivo temporal
    grafica_ruta = os.path.basename(temp_file.name)
    print(f"Ruta del archivo temporal: {temp_file.name}")

    # Crea el HTML para el PDF
    html = render_to_string('informe_pdf_emp.html', {
        'empleados': empleados,
        'fecha_actual': fecha_actual,
        'grafica': temp_file.name,
        'logo': 'path_to_logo',  # Cambia por la ruta de tu logo
        'total_empleados': total_empleados,
        'empleados_activos': empleados_activos,
        'empleados_inactivos': empleados_inactivos
    })

    # Convierte el HTML a PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="informe_empleados.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)

    # Eliminar el archivo temporal después de generar el PDF
    #os.remove(temp_file.name)

    if pisa_status.err:
        return HttpResponse('Error al generar el PDF')
    return response

#genera infromes de productos
def generar_informe(request):
    productos = Producto.objects.filter(activo=True)
    fecha_actual = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    grafica_buffer = generar_grafica()
    grafica_buffer2 = grafica_pastel()
    total_productos = productos.count()
    total_precio = productos.aggregate(total_precio=models.Sum('precio'))['total_precio'] or 0
    total_stock = productos.aggregate(total_stock=models.Sum('stock'))['total_stock'] or 0

    # Guardar la gráfica en un archivo temporal
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
    temp_file.write(grafica_buffer.getvalue())
    temp_file.close()
    
    temp_file2 = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
    temp_file2.write(grafica_buffer2.getvalue())
    temp_file2.close()

    # Usa la ruta relativa del archivo temporal
    grafica_ruta = os.path.basename(temp_file.name)
    # Imprime la ruta para depuración
    print(f"Ruta del archivo temporal: {temp_file.name}")
    print(f"Ruta del archivo temporal: {temp_file2.name}")

    # Crea el HTML para el PDF
    html = render_to_string('informe_pdf.html', {
        'productos': productos,
        'fecha_actual': fecha_actual,
        'grafica': temp_file.name,
        'grafica2': temp_file2.name,
        'logo': 'path_to_logo',
        'total_productos': total_productos,
        'total_precio': total_precio,
        'total_stock': total_stock
    })

    # Convierte el HTML a PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="informe_productos.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)

    # Eliminar el archivo temporal después de generar el PDF
    #os.remove(temp_file.name)

    if pisa_status.err:
        return HttpResponse('Error al generar el PDF')
    return response

#Genera infromes de Clinetes
def generar_informe_clientes(request):
    clientes = Cliente.objects.all()
    fecha_actual = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    grafica_buffer = generar_grafica_clientes()
    
    total_clientes = clientes.count()
    clientes_activos = clientes.filter(activo=True).count()
    clientes_inactivos = clientes.filter(activo=False).count()

    # Guardar la gráfica en un archivo temporal
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
    temp_file.write(grafica_buffer.getvalue())
    temp_file.close()

    # Usa la ruta relativa del archivo temporal
    grafica_ruta = os.path.basename(temp_file.name)

    # Crea el HTML para el PDF
    html = render_to_string('informe_pdf_clientes.html', {
        'clientes': clientes,
        'fecha_actual': fecha_actual,
        'grafica': temp_file.name,
        'logo': 'path_to_logo',  # Cambia por la ruta de tu logo
        'total_clientes': total_clientes,
        'clientes_activos': clientes_activos,
        'clientes_inactivos': clientes_inactivos
    })

    # Convierte el HTML a PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="informe_clientes.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)

    # Eliminar el archivo temporal después de generar el PDF
    #os.remove(temp_file.name)

    if pisa_status.err:
        return HttpResponse('Error al generar el PDF')
    return response

#Informe porveedor
def generar_informe_proveedor(request):
    
    proveedores = Proveedor.objects.all()
    fecha_actual = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    grafica_buffer = generar_grafica_proveedores()
    
    total_proveedores = proveedores.count()
    proveedores_activos = proveedores.filter(activo=True).count()
    proveedores_inactivos = proveedores.filter(activo=False).count()

    # Guardar la gráfica en un archivo temporal
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
    temp_file.write(grafica_buffer.getvalue())
    temp_file.close()

    # Usa la ruta relativa del archivo temporal
    grafica_ruta = os.path.basename(temp_file.name)

    # Crea el HTML para el PDF
    html = render_to_string('informe_pdf_proveedores.html', {
        'proveedores': proveedores,
        'fecha_actual': fecha_actual,
        'grafica': temp_file.name,
        'logo': 'path_to_logo',  # Cambia por la ruta de tu logo
        'total_proveedores': total_proveedores,
        'proveedores_activos': proveedores_activos,
        'proveedores_inactivos': proveedores_inactivos
    })

    # Convierte el HTML a PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="informe_proveedores.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)

    # Eliminar el archivo temporal después de generar el PDF
    #os.remove(temp_file.name)

    if pisa_status.err:
        return HttpResponse('Error al generar el PDF')
    return response

def export_pdf_view(request):
    # Generar PDF
    html = render_to_string('export_pdf.html', {'data': 'some_data'})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="export.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)
    return response

#########
class add_venta(View):
    template_name = 'add_venta.html'

    def get(self, request, *args, **kwargs):
        venta_form = VentaForm()
        DetalleVentaFormSet = formset_factory(DetalleVentaForm, extra=1)
        detalle_formset = DetalleVentaFormSet()
        return render(request, self.template_name, {
            'venta_form': venta_form,
            'detalle_formset': detalle_formset,
            'total_venta': 0
        })

    def post(self, request, *args, **kwargs):
        venta_form = VentaForm(request.POST)
        DetalleVentaFormSet = formset_factory(DetalleVentaForm, extra=1)
        detalle_formset = DetalleVentaFormSet(request.POST)
        
        if venta_form.is_valid() and detalle_formset.is_valid():
            venta = venta_form.save(commit=False)
            total_venta = Decimal('0.00')
            
            # Primero guarda la instancia de venta
            venta.save()
            
            for detalle_form in detalle_formset:
                if detalle_form.cleaned_data:
                    producto = detalle_form.cleaned_data.get('producto')
                    cantidad = detalle_form.cleaned_data.get('cantidad')
                    if producto and cantidad:
                        precio_unitario = Decimal(producto.precio)
                        subtotal = Decimal(cantidad) * precio_unitario
                        iva = subtotal * Decimal('0.16')  # IVA del 16%
                        total = subtotal + iva
                        
                        detalle = detalle_form.save(commit=False)
                        detalle.venta = venta  # Asocia el detalle con la venta
                        detalle.precio_unitario = precio_unitario
                        detalle.subtotal = subtotal
                        detalle.iva = iva
                        detalle.total = total
                        detalle.save()
                        
                        producto.stock -= int(cantidad)
                        producto.save()
                        
                        total_venta += total
            
            venta.total = total_venta
            venta.save()
            return redirect('ventas_listar')  # Redirige a la lista de ventas o a otra página
        else:
            return render(request, self.template_name, {
                'venta_form': venta_form,
                'detalle_formset': detalle_formset,
                'total_venta': 0
            })
def ventas_listar(request):
    ventas = Venta.objects.all()
    return render(request, 'ventas_listar.html', {'ventas': ventas})
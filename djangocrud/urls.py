"""
URL configuration for djangocrud project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tasks import views
#from tasks.views import export_pdf_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home, name='home'),
    path('signup/',views.signup, name='signup'),
    path('tasks/',views.tasks, name='tasks'),
    path('empleados/',views.empleados, name='empleados'),
    path('clientes/',views.clientes, name='clientes'),
    path('proveedor/',views.proveedor, name='proveedor'),
    path('venta/',views.venta, name='venta'),
    path('logout/',views.signup, name='logout'),
    path('signin/',views.signin, name='signin'),
    path('tasks/crear_producto/',views.crear_producto, name='crear_producto'),
    path('empleados/crear_empleado/',views.crear_empleado, name='crear_empleado'),
    path('clientes/crear_clientes/',views.crear_clientes, name='crear_clientes'),
    path('proveedor/crear_proveedor/',views.crear_proveedor, name='crear_proveedor'),
    path('venta/crear_venta/',views.crear_venta, name='crear_venta'),
    path('tasks/eliminar_producto/<int:pk>/', views.eliminar_producto, name='eliminar_producto'),
    path('empleados/eliminar_empleado/<int:pk>/', views.eliminar_empleado, name='eliminar_empleado'),
    path('clientes/eliminar_clientes/<int:pk>/', views.eliminar_clientes, name='eliminar_clientes'),
    path('proveedor/eliminar_proveedor/<int:pk>/', views.eliminar_proveedor, name='eliminar_proveedor'),
    #path('venta/eliminar_venta/<int:pk>/', views.eliminar_venta, name='eliminar_venta'),
    path('producto/<int:pk>/editar/', views.editar_producto, name='editar_producto'),
    path('empleados/<int:pk>/editar/', views.editar_empleado, name='editar_empleado'),
    path('clientes/<int:pk>/editar/', views.editar_clientes, name='editar_clientes'),
    path('proveedor/<int:pk>/editar/', views.editar_proveedor, name='editar_proveedor'),
    #path('venta/<int:pk>/editar/', views.editar_venta, name='editar_venta'),
    path('producto/<int:pk>/ver/', views.ver_producto, name='ver_producto'),
    path('empleados/<int:pk>/ver/', views.ver_empleado, name='ver_empleado'),
    path('clientes/<int:pk>/ver/', views.ver_clientes, name='ver_clientes'),
    path('proveedor/<int:pk>/ver/', views.ver_proveedor, name='ver_proveedor'),
    #path('venta/<int:pk>/ver/', views.ver_venta, name='ver_venta'),
    path('informe/', views.generar_informe, name='generar_informe'), 
    path('informe_empleados/', views.generar_informe_empleados, name='generar_informe_empleados'),
    path('informe_clientes/', views.generar_informe_clientes, name='generar_informe_clientes'), 
    path('informe_proveedor/', views.generar_informe_proveedor, name='generar_informe_proveedor'),    
    #path('informe_venta/', views.generar_informe_venta, name='generar_informe_venta'),    
    path('add_venta/', views.add_venta.as_view(), name='AddVenta'),
    
    path('export/', views.export_pdf_view, name="ExportPDF"),
    path('export/<id>/<iva>/', views.export_pdf_view, name="ExportPDF"),
]


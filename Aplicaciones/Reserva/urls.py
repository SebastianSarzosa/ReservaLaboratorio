from django.urls import path
from . import views

urlpatterns = [
    #Facultades 
    path('', views.home, name="home"),
    path('registrarFacultad/', views.registrarFacultad, name='registrarFacultad'),
    path('gestionFacultades/', views.gestionFacultades, name='registrarFacultades'),
    path('eliminarFacultad/<int:id>/', views.eliminarFacultad, name='eliminarFacultad'),
    path('facultad/editar/<int:facultad_id>/', views.editar_facultad, name='editarFacultad'),
    #Laboratorios:
    path('laboratorios/', views.gestionLaboratorios, name='gestionLaboratorios'),
    path('laboratorios/registrar/', views.registrarLaboratorio, name='registrarLaboratorio'),
    path('laboratorios/eliminar/<int:id>/', views.eliminarLaboratorio, name='eliminarLaboratorio'),
    path('laboratorios/editar/<int:laboratorio_id>/', views.editarLaboratorio, name='editarLaboratorio'),


    path('reservas/calendario/', views.calendario_reservas, name='calendarioReservas'),
    path('reservas/agregar/', views.agregar_reserva, name='agregarReserva'),
    path('reservas/obtener/', views.obtener_reservas, name='obtenerReservas'),
    path('reservas/eliminar/<int:id>/', views.eliminar_reserva, name='eliminar_reserva'),
]

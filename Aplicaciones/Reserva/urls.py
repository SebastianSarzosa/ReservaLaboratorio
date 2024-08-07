from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('registrarFacultad/', views.registrarFacultad, name='registrarFacultad'),
    path('gestionFacultades/', views.gestionFacultades, name='registrarFacultades'),
    path('eliminarFacultad/<int:id>/', views.eliminarFacultad, name='eliminarFacultad'),
    path('facultad/editar/<int:facultad_id>/', views.editar_facultad, name='editarFacultad'),
]

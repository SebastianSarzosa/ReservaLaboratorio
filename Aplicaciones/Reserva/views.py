from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from .models import Facultad


#Este es el modelo principal
def home(request):
    return render(request, "base.html")

#Este es para mostrar las facultades 

def gestionFacultades(request):
    return render(request, "gestionFacultades.html", {
        'facultades': Facultad.objects.all()
    })


#Este es para registrar lo que son las facultades 

def registrarFacultad(request):
    if request.method == 'POST':
        # Obtén los datos del formulario
        nombre = request.POST.get('txtNombre')
        descripcion = request.POST.get('txtDescripcion', '')  # Usa un valor predeterminado si está vacío

        # Verifica si ya existe una facultad con el mismo nombre
        if Facultad.objects.filter(nombre=nombre).exists():
            messages.error(request, 'La facultad ya existe.')
        else:
            # Crea una nueva instancia de Facultad
            Facultad.objects.create(
                nombre=nombre, 
                descripcion=descripcion
            )
            # Muestra un mensaje de éxito
            messages.success(request, '¡Facultad registrada con éxito!')

        # Redirige a la página de gestión de facultades
        return redirect('registrarFacultades')  # Asegúrate de que esta URL esté configurada correctamente en urls.py

    # En caso de GET, simplemente renderiza el formulario
    return render(request, 'gestionFacultades.html', {
        'facultades': Facultad.objects.all()
    })

#Este es para eliminar la facultad 

def eliminarFacultad(request, id):
    # Obtén la facultad a eliminar
    facultad = get_object_or_404(Facultad, id=id)

    # Elimina la facultad
    facultad.delete()

    # Muestra un mensaje de éxito
    messages.success(request, '¡Facultad eliminada con éxito!')

    # Redirige a la página de gestión de facultades
    return redirect('registrarFacultades')

#Editar facultad 

def editar_facultad(request, facultad_id):
    facultad = get_object_or_404(Facultad, id=facultad_id)
    
    if request.method == 'POST':
        nombre = request.POST.get('txtNombre')
        descripcion = request.POST.get('txtDescripcion', '')

        if not nombre:
            messages.error(request, 'El nombre de la facultad es obligatorio.')
        else:
            facultad.nombre = nombre
            facultad.descripcion = descripcion
            facultad.save()
            messages.success(request, 'Facultad actualizada exitosamente.')
            return redirect('registrarFacultad')  # Asume que este es el nombre de la URL para listar las facultades

    context = {
        'facultad': facultad
    }
    return render(request, 'editar_facultad.html', context)
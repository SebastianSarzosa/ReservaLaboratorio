from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.utils.dateparse import parse_date, parse_time

from Aplicaciones import Reserva
from .models import Facultad, Laboratorio,Reserva


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








#Laboratorios 

def gestionLaboratorios(request):
    laboratorios = Laboratorio.objects.all()
    facultades = Facultad.objects.all()  # Obtener todas las facultades para el formulario

    return render(request, "gestionLaboratorios.html", {
        'laboratorios': laboratorios,
        'facultades': facultades
    })

def registrarLaboratorio(request):
    if request.method == 'POST':
        nombre = request.POST.get('txtNombre')
        capacidad = request.POST.get('txtCapacidad')
        descripcion = request.POST.get('txtDescripcion', '')
        facultad_id = request.POST.get('selFacultad')

        if not nombre or not capacidad or not facultad_id:
            messages.error(request, 'Todos los campos son obligatorios.')
        else:
            try:
                capacidad = int(capacidad)
                facultad = Facultad.objects.get(id=facultad_id)

                if Laboratorio.objects.filter(nombre=nombre).exists():
                    messages.error(request, 'El laboratorio ya existe.')
                else:
                    Laboratorio.objects.create(
                        nombre=nombre,
                        capacidad=capacidad,
                        descripcion=descripcion,
                        facultad=facultad
                    )
                    messages.success(request, '¡Laboratorio registrado con éxito!')

            except Facultad.DoesNotExist:
                messages.error(request, 'La facultad seleccionada no es válida.')
            except ValueError:
                messages.error(request, 'La capacidad debe ser un número entero.')

    return redirect('gestionLaboratorios')

def eliminarLaboratorio(request, id):
    laboratorio = get_object_or_404(Laboratorio, id=id)
    laboratorio.delete()
    messages.success(request, '¡Laboratorio eliminado con éxito!')
    return redirect('gestionLaboratorios')

def editarLaboratorio(request, laboratorio_id):
    laboratorio = get_object_or_404(Laboratorio, id=laboratorio_id)

    if request.method == 'POST':
        nombre = request.POST.get('txtNombre')
        capacidad = request.POST.get('txtCapacidad')
        descripcion = request.POST.get('txtDescripcion', '')
        facultad_id = request.POST.get('selFacultad')

        if not nombre or not capacidad or not facultad_id:
            messages.error(request, 'Todos los campos son obligatorios.')
        else:
            try:
                capacidad = int(capacidad)
                facultad = Facultad.objects.get(id=facultad_id)

                laboratorio.nombre = nombre
                laboratorio.capacidad = capacidad
                laboratorio.descripcion = descripcion
                laboratorio.facultad = facultad
                laboratorio.save()

                messages.success(request, 'Laboratorio actualizado exitosamente.')
                return redirect('gestionLaboratorios')

            except Facultad.DoesNotExist:
                messages.error(request, 'La facultad seleccionada no es válida.')
            except ValueError:
                messages.error(request, 'La capacidad debe ser un número entero.')

    facultades = Facultad.objects.all()  # Obtener todas las facultades para el formulario
    context = {
        'laboratorio': laboratorio,
        'facultades': facultades
    }
    return render(request, 'editar_laboratorio.html', context)







def calendario_reservas(request):
    laboratorios = Laboratorio.objects.all()
    reservas = Reserva.objects.all()

    # Serializar reservas para enviarlas al cliente
    eventos = [
        {
            'id': reserva.id,
            'title': f"{reserva.usuario} ({reserva.motivo})",
            'start': f"{reserva.fecha}T{reserva.hora_inicio}",
            'end': f"{reserva.fecha}T{reserva.hora_fin}",
            'laboratorio': reserva.laboratorio.nombre,
        }
        for reserva in reservas
    ]

    return render(request, 'calendario_reservas.html', {
        'laboratorios': laboratorios,
        'eventos': eventos,
    })

def agregar_reserva(request):
    if request.method == 'POST':
        usuario = request.POST.get('usuario')
        laboratorio_id = request.POST.get('laboratorio')
        fecha = parse_date(request.POST.get('fecha'))
        hora_inicio = parse_time(request.POST.get('hora_inicio'))
        hora_fin = parse_time(request.POST.get('hora_fin'))
        motivo = request.POST.get('motivo')

        if not usuario or not laboratorio_id or not fecha or not hora_inicio or not hora_fin or not motivo:
            messages.error(request, 'Todos los campos son obligatorios.')
            return redirect('calendarioReservas')

        laboratorio = get_object_or_404(Laboratorio, id=laboratorio_id)

        # Verificar conflictos de reserva
        conflictos = Reserva.objects.filter(
            laboratorio=laboratorio,
            fecha=fecha,
            hora_inicio__lt=hora_fin,
            hora_fin__gt=hora_inicio
        ).exists()

        if conflictos:
            messages.error(request, 'El laboratorio ya está reservado en este horario.')
            return redirect('calendarioReservas')

        Reserva.objects.create(
            usuario=usuario,
            laboratorio=laboratorio,
            fecha=fecha,
            hora_inicio=hora_inicio,
            hora_fin=hora_fin,
            motivo=motivo
        )
        messages.success(request, 'Reserva realizada con éxito.')
        return redirect('calendarioReservas')

    return redirect('calendarioReservas')

def obtener_reservas(request):
    reservas = Reserva.objects.all()

    # Serializar reservas para enviarlas como JSON
    eventos = [
        {
            'id': reserva.id,
            'title': f"{reserva.usuario} ({reserva.motivo})",
            'start': f"{reserva.fecha}T{reserva.hora_inicio}",
            'end': f"{reserva.fecha}T{reserva.hora_fin}",
            'laboratorio': reserva.laboratorio.nombre,
        }
        for reserva in reservas
    ]
    return JsonResponse(eventos, safe=False)



def eliminar_reserva(request, id):
    if request.method == 'DELETE':
        reserva = get_object_or_404(Reserva, id=id)
        reserva.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)
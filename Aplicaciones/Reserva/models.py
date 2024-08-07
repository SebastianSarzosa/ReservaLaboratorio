from django.db import models

# Create your models here.

class Facultad(models.Model):
    id = models.AutoField(primary_key=True)  # ID personalizado
    nombre = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre


class Laboratorio(models.Model):
    id = models.AutoField(primary_key=True)  # ID personalizado
    nombre = models.CharField(max_length=255, unique=True)
    capacidad = models.PositiveIntegerField()
    facultad = models.ForeignKey(Facultad, on_delete=models.CASCADE, related_name='laboratorios')
    descripcion = models.TextField(blank=True, null=True)
    foto = models.FileField(upload_to='laboratorio', max_length=100, default="hola mundo")


    def __str__(self):
        return self.nombre


class Reserva(models.Model):
    id = models.AutoField(primary_key=True)  # ID personalizado
    usuario = models.CharField(max_length=255)
    laboratorio = models.ForeignKey(Laboratorio, on_delete=models.CASCADE, related_name='reservas')
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    motivo = models.TextField()

    def __str__(self):
        return f"Reserva de {self.usuario} en {self.laboratorio} el {self.fecha}"


class Usuario(models.Model):
    id = models.AutoField(primary_key=True)  # ID personalizado
    nombre = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.nombre


class Equipo(models.Model):
    id = models.AutoField(primary_key=True)  # ID personalizado
    nombre = models.CharField(max_length=255)
    laboratorio = models.ForeignKey(Laboratorio, on_delete=models.CASCADE, related_name='equipos')
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre


class Horario(models.Model):
    id = models.AutoField(primary_key=True)  # ID personalizado
    laboratorio = models.ForeignKey(Laboratorio, on_delete=models.CASCADE, related_name='horarios')
    dia = models.CharField(max_length=9)  # Ej. "Lunes", "Martes"
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    def __str__(self):
        return f"{self.laboratorio} - {self.dia} {self.hora_inicio} - {self.hora_fin}"

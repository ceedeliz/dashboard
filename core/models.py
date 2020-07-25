from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Project(models.Model):
    @property
    def prueba(self):
        return "pruebapython"

    def pruebaint(self):
        return 10

    title = models.CharField(max_length = 100, default="Título de prueba",verbose_name = "Título") 
    content = models.TextField(default="Contenido de prueba",verbose_name = "Contenido")
    date_posted = models.DateTimeField(default=timezone.now,verbose_name = "Fecha")
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1, verbose_name = "Autor")

    class Meta:
        verbose_name = "Proyecto"
        verbose_name_plural ="Proyectos"
        ordering = ["-date_posted"]

    def __str__(self):
        return self.title
    
class Post(models.Model):
    title = models.CharField(max_length = 100, default="Título de prueba") 
    content = models.TextField(default="Contenido de prueba")
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    
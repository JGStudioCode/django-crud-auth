from django.db import models
# Modelo de la tabla user que crea Django
from django.contrib.auth.models import User

# Create your models here.

#Modelo Tareas
class Task(models.Model):
    title =  models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now=True)
    datecompleted = models.DateTimeField(null=True, blank=True) #blank=True para acepte vacios solo desde el ADMIN
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # Anadir vista al ADMIN
    def __str__(self):
        return self.title + ' by ' + self.user.username
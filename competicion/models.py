from django.db import models

class Competicion(models.Model):
    nombre = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.nombre

class Entrenador(models.Model):
    nombre = models.CharField(max_length=200)
    def __str__(self):
        return self.nombre

class Resultado(models.Model):
    entrenador_casa = models.ForeignKey(Entrenador, on_delete=models.CASCADE, related_name='casa')
    entrenador_fuera = models.ForeignKey(Entrenador, on_delete=models.CASCADE, related_name='fuera')
    td_casa= models.IntegerField(default=0)
    td_fuera= models.IntegerField(default=0)
    competicion = models.ForeignKey(Competicion, on_delete=models.CASCADE)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return f'{self.entrenador_casa} vs {self.entrenador_fuera.nombre} ({self.td_casa}-{self.td_fuera})'
from djongo import models

class DatosRed(models.Model):
    _id = models.ObjectIdField()
    tipo = models.IntegerField()
    entrada = models.FloatField()
    salida = models.FloatField()
    createdAt = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta: 
        app_label = 'database'

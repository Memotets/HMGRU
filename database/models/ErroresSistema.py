from djongo import models

class ErroresSistema(models.Model):
    _id = models.ObjectIdField()
    codigo = models.IntegerField()
    mensaje = models.TextField()
    moduloOiren = models.TextField()
    createdAt = models.DateTimeField( auto_now=False, auto_now_add=True)

    class Meta: 
        app_label = 'database'
from djongo import models

class Edificio(models.Model):
    nombre = models.TextField()
    ip = models.TextField()

    class Meta: 
        abstract = True
        app_label = 'database'
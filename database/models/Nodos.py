from djongo import models
from database.models.Edificio import Edificio

class Nodo(models.Model):
    _id = models.ObjectIdField
    identificadorCable = models.TextField()
    idPuerto = models.TextField()
    edificio = models.EmbeddedField(
        model_container=Edificio
    )
    lugar = models.TextField()
    planta = models.TextField()
    vlan = models.TextField()
    ip = models.TextField()
    usuario = models.TextField()
    activoAdministrativo = models.BooleanField()

    class Meta:
        abstract = True
        app_label = 'database'
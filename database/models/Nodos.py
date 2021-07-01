from djongo import models
from database.models.Edificio import Edificio

class Nodos(models.Model):
    _id = models.ObjectIdField
    oid = models.TextField()
    identificadorCable = models.TextField()
    idPuerto = models.TextField()
    edificio = models.EmbeddedField(
        model_container=Edificio,
        null = True
    )
    lugar = models.TextField()
    planta = models.TextField()
    vlan = models.TextField()
    ip = models.TextField(null=True)
    usuario = models.TextField()
    activoAdministrativo = models.BooleanField()

    class Meta:
        app_label = 'database'
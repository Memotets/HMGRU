from djongo import models

from database.models.Edificio import Edificio
from database.models.Nodos import Nodos

class DatosRed(models.Model):
    _id = models.ObjectIdField()
    tipo = models.IntegerField()
    entrada = models.FloatField()
    salida = models.FloatField()
    edificio = models.EmbeddedField(
        model_container=Edificio,
        null = True
    )
    nodo = models.ForeignKey(to=Nodos, on_delete=models.DO_NOTHING, null=True, related_name='Nodo', db_column='Nodo')
    createdAt = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return "(tipo: %i, entrada: %f, salida: %f)" %(self.tipo, self.entrada, self.salida)

    class Meta: 
        app_label = 'database'

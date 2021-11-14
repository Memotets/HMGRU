from djongo  import models

from database.models.Edificio import Edificio

class Media(models.Model):
    valor = models.FloatField()

    def __str__(self):
        return "%f" %(self.valor)

    class Meta:
        abstract = True
        app_label = 'database'

class topNodo(models.Model):
    nodo = models.TextField(null=False)
    mediaTotal = models.FloatField()
    mediaEntrada = models.FloatField()
    mediaSalida = models.FloatField()

    class Meta:
        app_label = 'database'
        abstract = True

class Reporte(models.Model):
    _id = models.ObjectIdField()
    tipo = models.IntegerField()
    mediaTotal = models.ArrayField(model_container=Media)
    mediaEntrada = models.ArrayField(model_container=Media)
    mediaSalida = models.ArrayField(model_container=Media)
    topNodos = models.ArrayField(model_container=topNodo)
    edificio = models.EmbeddedField(
        model_container=Edificio,
        null = True,
        db_column='Edificio'
    )
    diaReportado = models.DateField(auto_now=False, auto_now_add=False)

    class Meta:
        app_label = 'database'


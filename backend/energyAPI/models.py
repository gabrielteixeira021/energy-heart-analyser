from django.db import models

# Create your models here.
# Dados: hora,temperatura_c,radiacao_wm2,potencia_kw
class DesempenhoPainelSolar(models.Model):
    painel_solar_id = models.IntegerField(primary_key=True)
    hora = models.IntegerField()
    radiacao_wm2 = models.FloatField()
    temperatura = models.FloatField()
    potencia_km = models.FloatField()
    
    def __str__(self):
        return f"Painel Solar: {self.painel_solar_id}"

    
    
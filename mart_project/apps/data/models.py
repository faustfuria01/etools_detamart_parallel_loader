from django.db import models

# Stub source models
class PartnersPartnerorganization(models.Model):
    name = models.CharField(max_length=255)

class T2FTravelactivity(models.Model):
    travel_type = models.CharField(max_length=50)
    date = models.DateField(null=True)
    travels_status = models.CharField(max_length=50)
    primary_traveler = models.IntegerField()

class TravelType:
    PROGRAMME_MONITORING = 'PROGRAMME_MONITORING'
from django.db import models
from django.contrib.auth.models import User
import uuid

# geniehenri@gmail.com / geniehenri

class Patient(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    details = models.JSONField()

class SPECIALITE(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=100)

class Doctor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialite = models.ForeignKey(SPECIALITE, on_delete=models.CASCADE)

class Creneau(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    day = models.SmallIntegerField()
    start_time = models.TimeField()
    end_time = models.TimeField()

class RendezVous(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    creneau = models.ForeignKey(Creneau, on_delete=models.CASCADE)
    approved_by = models.ForeignKey(User, on_delete=models.PROTECT)
    approved_at = models.DateTimeField()
    heure = models.DateTimeField()

class Consultation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rendez_vous = models.OneToOneField(RendezVous, on_delete=models.CASCADE)
    notes = models.TextField()
    prescription = models.JSONField()

class PaymentMethod(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    numero = models.CharField(max_length=100)
    libelle = models.CharField(max_length=100)
    description = models.TextField()

class Paiement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rendez_vous = models.OneToOneField(RendezVous, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="paiements/")
    approved_by = models.ForeignKey(User, on_delete=models.PROTECT)
    approved_at = models.DateTimeField()


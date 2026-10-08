from django.db import models
from django.contrib.auth.models import User
import uuid

# geniehenri@gmail.com / geniehenri

class Patient(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    details = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username

class SPECIALITE(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

class Doctor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialite = models.ForeignKey(SPECIALITE, on_delete=models.CASCADE)

    def __str__(self):
        return f"Dr {self.user.get_full_name() or self.user.username}"

class Creneau(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    day = models.SmallIntegerField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.doctor} - jour {self.day} ({self.start_time:%H:%M}-{self.end_time:%H:%M})"

class RendezVous(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    creneau = models.ForeignKey(Creneau, on_delete=models.CASCADE)
    approved_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name="%(class)s_approuves")
    approved_at = models.DateTimeField(null=True, blank=True)
    heure = models.DateTimeField()

    def __str__(self):
        return f"{self.patient} / {self.doctor} - {self.heure:%Y-%m-%d %H:%M}"

class Consultation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rendez_vous = models.OneToOneField(RendezVous, on_delete=models.CASCADE)
    notes = models.TextField()
    prescription = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"Consultation {self.rendez_vous}"

class PaymentMethod(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    numero = models.CharField(max_length=100)
    libelle = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return f"{self.libelle} ({self.numero})"

class Paiement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rendez_vous = models.OneToOneField(RendezVous, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="paiements/")
    approved_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name="%(class)s_approuves")
    approved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.amount} - {self.rendez_vous}"

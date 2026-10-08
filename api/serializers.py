from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active']

class ObtainTokenPairWithUserSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = UserSerializer(self.user).data
        return data

class SpecialiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SPECIALITE
        fields = "__all__"

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = UserSerializer(instance.user).data
        return representation

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = UserSerializer(instance.user).data
        representation['specialite'] = SpecialiteSerializer(instance.specialite).data
        return representation

class CreneauSerializer(serializers.ModelSerializer):
    class Meta:
        model = Creneau
        fields = "__all__"

    def validate_day(self, value):
        if not 0 <= value <= 6:
            raise serializers.ValidationError("Le jour doit être compris entre 0 (lundi) et 6 (dimanche).")
        return value

    def validate(self, attrs):
        start_time = attrs.get('start_time', getattr(self.instance, 'start_time', None))
        end_time = attrs.get('end_time', getattr(self.instance, 'end_time', None))
        if start_time and end_time and start_time >= end_time:
            raise serializers.ValidationError("L'heure de début doit être avant l'heure de fin.")
        return attrs

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['doctor'] = str(instance.doctor)
        representation['doctor_id'] = str(instance.doctor_id)
        return representation

class RendezVousSerializer(serializers.ModelSerializer):
    class Meta:
        model = RendezVous
        fields = "__all__"
        read_only_fields = ['approved_by', 'approved_at']

    def validate(self, attrs):
        doctor = attrs.get('doctor', getattr(self.instance, 'doctor', None))
        creneau = attrs.get('creneau', getattr(self.instance, 'creneau', None))
        heure = attrs.get('heure', getattr(self.instance, 'heure', None))
        if doctor and creneau and creneau.doctor_id != doctor.id:
            raise serializers.ValidationError({'creneau': "Ce créneau n'appartient pas à ce médecin."})
        if creneau and heure:
            if heure.weekday() != creneau.day or not creneau.start_time <= heure.time() < creneau.end_time:
                raise serializers.ValidationError({'heure': "L'heure ne correspond pas au créneau choisi."})
        return attrs

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['patient'] = PatientSerializer(instance.patient).data
        representation['doctor'] = DoctorSerializer(instance.doctor).data
        representation['creneau'] = CreneauSerializer(instance.creneau).data
        representation['approved_by'] = str(instance.approved_by) if instance.approved_by else None
        return representation

class ConsultationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consultation
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['rendez_vous'] = RendezVousSerializer(instance.rendez_vous).data
        return representation

class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = "__all__"

class PaiementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paiement
        fields = "__all__"
        read_only_fields = ['approved_by', 'approved_at']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['rendez_vous'] = str(instance.rendez_vous)
        representation['rendez_vous_id'] = str(instance.rendez_vous_id)
        representation['approved_by'] = str(instance.approved_by) if instance.approved_by else None
        return representation

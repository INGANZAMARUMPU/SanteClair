from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'specialites', SpecialiteViewSet, basename='specialite')
router.register(r'patients', PatientViewSet, basename='patient')
router.register(r'doctors', DoctorViewSet, basename='doctor')
router.register(r'creneaux', CreneauViewSet, basename='creneau')
router.register(r'rendez-vous', RendezVousViewSet, basename='rendezvous')
router.register(r'consultations', ConsultationViewSet, basename='consultation')
router.register(r'payment-methods', PaymentMethodViewSet, basename='paymentmethod')
router.register(r'paiements', PaiementViewSet, basename='paiement')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', ObtainTokenPair.as_view(), name='token_obtain_pair'),
]

from django.utils import timezone
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import *

class ObtainTokenPair(TokenObtainPairView):
    serializer_class = ObtainTokenPairWithUserSerializer

class BaseViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication, SessionAuthentication]

class ApprovableViewSet(BaseViewSet):
    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def approve(self, request, pk=None):
        instance = self.get_object()
        instance.approved_by = request.user
        instance.approved_at = timezone.now()
        instance.save(update_fields=['approved_by', 'approved_at'])
        return Response(self.get_serializer(instance).data)

class UserViewSet(ReadOnlyModelViewSet):
    queryset = User.objects.all().order_by('username')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication, SessionAuthentication]

class SpecialiteViewSet(BaseViewSet):
    queryset = SPECIALITE.objects.all().order_by('nom')
    serializer_class = SpecialiteSerializer

class PatientViewSet(BaseViewSet):
    queryset = Patient.objects.select_related('user').order_by('user__last_name', 'user__first_name')
    serializer_class = PatientSerializer

class DoctorViewSet(BaseViewSet):
    queryset = Doctor.objects.select_related('user', 'specialite').order_by('user__last_name', 'user__first_name')
    serializer_class = DoctorSerializer

class CreneauViewSet(BaseViewSet):
    queryset = Creneau.objects.select_related('doctor__user').order_by('day', 'start_time')
    serializer_class = CreneauSerializer

class RendezVousViewSet(ApprovableViewSet):
    queryset = RendezVous.objects.select_related(
        'patient__user', 'doctor__user', 'doctor__specialite', 'creneau__doctor__user', 'approved_by'
    ).order_by('-heure')
    serializer_class = RendezVousSerializer

class ConsultationViewSet(BaseViewSet):
    queryset = Consultation.objects.select_related(
        'rendez_vous__patient__user', 'rendez_vous__doctor__user', 'rendez_vous__doctor__specialite',
        'rendez_vous__creneau__doctor__user', 'rendez_vous__approved_by'
    ).order_by('-rendez_vous__heure')
    serializer_class = ConsultationSerializer

class PaymentMethodViewSet(BaseViewSet):
    queryset = PaymentMethod.objects.all().order_by('libelle')
    serializer_class = PaymentMethodSerializer

class PaiementViewSet(ApprovableViewSet):
    queryset = Paiement.objects.select_related(
        'rendez_vous__patient__user', 'rendez_vous__doctor__user', 'approved_by'
    ).order_by('-rendez_vous__heure')
    serializer_class = PaiementSerializer

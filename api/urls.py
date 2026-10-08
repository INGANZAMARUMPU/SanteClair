from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'postes', PosteViewSet, basename='poste')
router.register(r'personnels', PersonnelViewSet, basename='personnel')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', ObtainTokenPair.as_view(), name='token_obtain_pair'),
]

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from unfold.admin import ModelAdmin
from unfold.contrib.import_export.forms import ImportForm, SelectableFieldsExportForm
from import_export.admin import ImportExportModelAdmin

from .models import *

admin.site.unregister(User)

@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    # Forms loaded from `unfold.forms`
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm

@admin.register(SPECIALITE)
class SpecialiteAdmin(ModelAdmin):
    list_display = ('id', 'nom')
    search_fields = ('nom',)

@admin.register(Patient)
class PatientAdmin(ModelAdmin, ImportExportModelAdmin):
    import_form_class = ImportForm
    export_form_class = SelectableFieldsExportForm
    list_display = ('id', 'user', 'details')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'user__email')
    autocomplete_fields = ('user',)

@admin.register(Doctor)
class DoctorAdmin(ModelAdmin, ImportExportModelAdmin):
    import_form_class = ImportForm
    export_form_class = SelectableFieldsExportForm
    list_display = ('id', 'user', 'specialite')
    list_filter = ('specialite',)
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'specialite__nom')
    autocomplete_fields = ('user', 'specialite')

@admin.register(Creneau)
class CreneauAdmin(ModelAdmin):
    list_display = ('id', 'doctor', 'day', 'start_time', 'end_time')
    list_filter = ('day', 'doctor')
    search_fields = ('doctor__user__username', 'doctor__user__first_name', 'doctor__user__last_name')
    autocomplete_fields = ('doctor',)

@admin.register(RendezVous)
class RendezVousAdmin(ModelAdmin):
    list_display = ('id', 'patient', 'doctor', 'creneau', 'heure', 'approved_by', 'approved_at')
    list_filter = ('doctor', 'approved_at')
    search_fields = ('patient__user__username', 'patient__user__last_name', 'doctor__user__username', 'doctor__user__last_name')
    autocomplete_fields = ('patient', 'doctor', 'creneau', 'approved_by')
    date_hierarchy = 'heure'

@admin.register(Consultation)
class ConsultationAdmin(ModelAdmin):
    list_display = ('id', 'rendez_vous', 'notes')
    search_fields = ('rendez_vous__patient__user__username', 'rendez_vous__doctor__user__username', 'notes')
    autocomplete_fields = ('rendez_vous',)

@admin.register(PaymentMethod)
class PaymentMethodAdmin(ModelAdmin):
    list_display = ('id', 'nom', 'libelle', 'numero', 'description')
    search_fields = ('libelle', 'numero')

@admin.register(Paiement)
class PaiementAdmin(ModelAdmin):
    list_display = ('id', 'rendez_vous', 'amount', 'image', 'approved_by', 'approved_at')
    list_filter = ('approved_at',)
    search_fields = ('rendez_vous__patient__user__username', 'rendez_vous__doctor__user__username')
    autocomplete_fields = ('rendez_vous', 'approved_by')

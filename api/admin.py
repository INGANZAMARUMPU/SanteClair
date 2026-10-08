from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from unfold.admin import ModelAdmin
from unfold.contrib.import_export.forms import ExportForm, ImportForm, SelectableFieldsExportForm

from .models import *

@admin.register(User)
class UserAdmin(UserAdmin, ModelAdmin):
    # Forms loaded from `unfold.forms`
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm

@admin.register(Poste)
class PosteAdmin(ModelAdmin):
    list_display = ('id', 'nom')
    search_fields = ('nom',)

@admin.register(Personnel)
class PersonnelAdmin(ModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm
    export_form_class = SelectableFieldsExportForm
    list_display = ('id', 'nom', 'prenom', 'poste', 'email', 'telephone', 'photo')
    search_fields = ('nom', 'prenom', 'poste__nom')
    autocomplete_fields = ('poste', )

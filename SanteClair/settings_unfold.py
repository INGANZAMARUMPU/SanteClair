from django.templatetags.static import static
from django.urls import reverse_lazy

def permission_callback(request, *permission_labels):
    for label in permission_labels:
        if request.user.has_perm(label):
            return True
    return False  

UNFOLD = {
    "SITE_TITLE": "SanteClair",
    "SITE_HEADER": "SanteClair Admin",
    "SITE_SUBHEADER": "Gestion de clinique",
    "SITE_URL": "/",
    # "DASHBOARD_CALLBACK": "AMHABadges.dashboard.dashboard_callback",
    # "SITE_ICON": lambda request: static("icon.svg"),  # both modes, optimise for 32px height
    # "SITE_ICON": {
    #     "light": lambda request: static("icon-light.svg"),  # light mode
    #     "dark": lambda request: static("icon-dark.svg"),  # dark mode
    # },
    # "SITE_LOGO": lambda request: static("logo.svg"),  # both modes, optimise for 32px height
    # "SITE_LOGO": {
    #     "light": lambda request: static("logo-light.svg"),  # light mode
    #     "dark": lambda request: static("logo-dark.svg"),  # dark mode
    # },
    # "SITE_SYMBOL": "speed",  # symbol from icon set
    # "SITE_FAVICONS": [
    #     {
    #         "rel": "icon",
    #         "sizes": "32x32",
    #         "type": "image/svg+xml",
    #         "href": lambda request: static("favicon.svg"),
    #     },
    # ],
    "SHOW_HISTORY": True, # show/hide "History" button, default: True
    "SHOW_VIEW_ON_SITE": True, # show/hide "View on site" button, default: True
    "SHOW_BACK_BUTTON": False, # show/hide "Back" button on changeform in header, default: False
    "SHOW_UI_WARNINGS": False, # show/hide warnings in UI, default: False
    "LOGIN": {
        # "image": lambda request: static("login-bg.jpg"),
        "redirect_after": lambda request: reverse_lazy("admin:index"),
        # Inherits from `unfold.forms.AuthenticationForm`
        # "form": "app.forms.CustomLoginForm",
    },
    # "STYLES": [
    #     lambda request: static("style.css"),
    # ],
    # "SCRIPTS": [
    #     lambda request: static("script.js"),
    # ],
    "BORDER_RADIUS": "6px",
    "COLORS": {
        "base": {
            "50": "oklch(98.5% .002 247.839)",
            "100": "oklch(96.7% .003 264.542)",
            "200": "oklch(92.8% .006 264.531)",
            "300": "oklch(87.2% .01 258.338)",
            "400": "oklch(70.7% .022 261.325)",
            "500": "oklch(55.1% .027 264.364)",
            "600": "oklch(44.6% .03 256.802)",
            "700": "oklch(37.3% .034 259.733)",
            "800": "oklch(27.8% .033 256.848)",
            "900": "oklch(21% .034 264.665)",
            "950": "oklch(13% .028 261.692)",
        },
        "primary": {
            "50": "239 246 255",
            "100": "219 234 254",
            "200": "191 219 254",
            "300": "147 197 253",
            "400": "96 165 250",
            "500": "59 130 246",
            "600": "37 99 235",
            "700": "29 78 216",
            "800": "30 64 175",
            "900": "30 58 138",
            "950": "23 37 84",
        },
        "font": {
            "subtle-light": "var(--color-base-500)",  # text-base-500
            "subtle-dark": "var(--color-base-400)",  # text-base-400
            "default-light": "var(--color-base-600)",  # text-base-600
            "default-dark": "var(--color-base-300)",  # text-base-300
            "important-light": "var(--color-base-900)",  # text-base-900
            "important-dark": "var(--color-base-100)",  # text-base-100
        },
    },
    "EXTENSIONS": {
        "modeltranslation": {
            "flags": {
                "en": "🇬🇧",
                "fr": "🇫🇷"
            },
        },
    },
    "SIDEBAR": {
        "show_search": True,  # Search in applications and models names
        "command_search": False,  # Replace the sidebar search with the command search
        "show_all_applications": True,  # Dropdown with all applications and models
        "navigation": [
            {
                "title": "Identités et Authorisations",
                "icon": "lock",
                "separator": True,
                "collapsible": True,
                "permission": lambda request: permission_callback(request, "auth.view_user", "auth.view_group"),
                "items": [
                    {
                        "title": "Users",
                        "icon": "people",
                        "link": reverse_lazy("admin:auth_user_changelist"),
                        "permission": lambda request: request.user.has_perm("auth.view_user"),
                    },
                    {
                        "title": "Groups",
                        "icon": "groups",
                        "link": reverse_lazy("admin:auth_group_changelist"),
                        "permission": lambda request: request.user.has_perm("auth.view_group"),
                    }
                ]
            },
            {
                "title": "Utilisateurs",
                "icon": "people",
                "separator": True,
                "collapsible": True,
                "permission": lambda request: permission_callback(request, "api.view_patient", "api.view_doctor"),
                "items": [
                    {
                        "title": "Patients",
                        "icon": "person",
                        "link": reverse_lazy("admin:api_patient_changelist"),
                        "permission": lambda request: request.user.has_perm("api.view_patient"),
                    },
                    {
                        "title": "Docteurs",
                        "icon": "medical_services",
                        "link": reverse_lazy("admin:api_doctor_changelist"),
                        "permission": lambda request: request.user.has_perm("api.view_doctor"),
                    }
                ]
            },
            {
                "title": "Rendez-vous & Consultations",
                "icon": "calendar_today",
                "separator": True,
                "collapsible": True,
                "permission": lambda request: permission_callback(request, "api.view_rendezvous", "api.view_consultation", "api.view_creneau", "api.view_specialite"),
                "items": [
                    {
                        "title": "Rendez-vous",
                        "icon": "event",
                        "link": reverse_lazy("admin:api_rendezvous_changelist"),
                        "permission": lambda request: request.user.has_perm("api.view_rendezvous"),
                    },
                    {
                        "title": "Consultations",
                        "icon": "stethoscope",
                        "link": reverse_lazy("admin:api_consultation_changelist"),
                        "permission": lambda request: request.user.has_perm("api.view_consultation"),
                    },
                    {
                        "title": "Créneaux",
                        "icon": "schedule",
                        "link": reverse_lazy("admin:api_creneau_changelist"),
                        "permission": lambda request: request.user.has_perm("api.view_creneau"),
                    },
                    {
                        "title": "Spécialités",
                        "icon": "category",
                        "link": reverse_lazy("admin:api_specialite_changelist"),
                        "permission": lambda request: request.user.has_perm("api.view_specialite"),
                    },
                ]
            },
            {
                "title": "Finances",
                "icon": "payments",
                "separator": True,
                "collapsible": True,
                "permission": lambda request: permission_callback(request, "api.view_paiement", "api.view_paymentmethod"),
                "items": [
                    {
                        "title": "Paiements",
                        "icon": "attach_money",
                        "link": reverse_lazy("admin:api_paiement_changelist"),
                        "permission": lambda request: request.user.has_perm("api.view_paiement"),
                    },
                    {
                        "title": "Méthodes de paiement",
                        "icon": "credit_card",
                        "link": reverse_lazy("admin:api_paymentmethod_changelist"),
                        "permission": lambda request: request.user.has_perm("api.view_paymentmethod"),
                    }
                ]
            }
        ],
    },
}
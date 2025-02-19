from django.apps import AppConfig


class PatientManagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'patient_management'

    def ready(self):
        import patient_management.signals  # Import signals

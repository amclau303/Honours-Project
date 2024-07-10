from django.core.management.base import BaseCommand
from thyroid.models import PatientData

class Command(BaseCommand):
    help = 'Clear all patient data from the database'

    def handle(self, *args, **kwargs):
        PatientData.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully cleared all patient data'))

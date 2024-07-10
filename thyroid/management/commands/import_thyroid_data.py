import csv
from django.core.management.base import BaseCommand
from thyroid.models import Thyroid  # Import your Thyroid model

class Command(BaseCommand):
    help = 'Imports data from ThyroidData.csv into the Thyroid model'

    def handle(self, *args, **options):
        file_path = 'C:/Users/Aaron/OneDrive - GLASGOW CALEDONIAN UNIVERSITY/4th Year/Honours Project/Project/honor/ThyroidData.csv'
        
        with open(file_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Handling empty or missing values gracefully
                gender = row.get('gender', '')
                treatment_status = row.get('treatment_status', '')
                thyroid_status = row.get('thyroid_status', '')
                
                # Convert year to integer and handle NULL string
                year = int(row['year']) if row['year'].strip() != '' else None
                
                thyroid_instance = Thyroid(
                    gender=gender,
                    treatment_status=treatment_status,
                    thyroid_status=thyroid_status,
                    year=year
                )
                thyroid_instance.save()
                self.stdout.write(self.style.SUCCESS(f'Successfully imported Thyroid data with year {row["year"]}'))

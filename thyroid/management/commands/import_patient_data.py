# myapp/management/commands/import_patient_data.py
import csv
from django.core.management.base import BaseCommand
from thyroid.models import PatientData

class Command(BaseCommand):
    help = 'Import patient data from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The path to the CSV file to be imported')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        def convert_to_bool(value):
            return value.strip().lower() == 't'

        def convert_to_float(value):
            try:
                return float(value)
            except (ValueError, TypeError):
                return None

        def clean_column_name(name):
            return name.strip().lower().replace(' ', '_')

        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                cleaned_row = {clean_column_name(k): v for k, v in row.items()}
                PatientData.objects.update_or_create(
                    patient_id=cleaned_row['patient_id'],
                    defaults={
                        'age': int(cleaned_row['age']),
                        'sex': cleaned_row['sex'],
                        'on_thyroxine': convert_to_bool(cleaned_row['on_thyroxine']),
                        'query_on_thyroxine': convert_to_bool(cleaned_row['query_on_thyroxine']),
                        'on_antithyroid_meds': convert_to_bool(cleaned_row['on_antithyroid_meds']),
                        'sick': convert_to_bool(cleaned_row['sick']),
                        'pregnant': convert_to_bool(cleaned_row['pregnant']),
                        'thyroid_surgery': convert_to_bool(cleaned_row['thyroid_surgery']),
                        'I131_treatment': convert_to_bool(cleaned_row['i131_treatment']),
                        'query_hypothyroid': convert_to_bool(cleaned_row['query_hypothyroid']),
                        'query_hyperthyroid': convert_to_bool(cleaned_row['query_hyperthyroid']),
                        'lithium': convert_to_bool(cleaned_row['lithium']),
                        'goitre': convert_to_bool(cleaned_row['goitre']),
                        'tumor': convert_to_bool(cleaned_row['tumor']),
                        'hypopituitary': convert_to_float(cleaned_row['hypopituitary']),
                        'psych': convert_to_bool(cleaned_row['psych']),
                        'TSH_measured': convert_to_bool(cleaned_row['tsh_measured']),
                        'TSH': convert_to_float(cleaned_row['tsh']),
                        'T3_measured': convert_to_bool(cleaned_row['t3_measured']),
                        'T3': convert_to_float(cleaned_row['t3']),
                        'TT4_measured': convert_to_bool(cleaned_row['tt4_measured']),
                        'TT4': convert_to_float(cleaned_row['tt4']),
                        'T4U_measured': convert_to_bool(cleaned_row['t4u_measured']),
                        'T4U': convert_to_float(cleaned_row['t4u']),
                        'FTI_measured': convert_to_bool(cleaned_row['fti_measured']),
                        'FTI': convert_to_float(cleaned_row['fti']),
                        'TBG_measured': convert_to_bool(cleaned_row['tbg_measured']),
                        'TBG': convert_to_float(cleaned_row['tbg']),
                        'referral_source': cleaned_row['referral_source'],
                        'target': cleaned_row['target'],
                    }
                )

        self.stdout.write(self.style.SUCCESS(f"Successfully imported data from {csv_file}"))

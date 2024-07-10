# import_locations.py
import csv
from django.core.management.base import BaseCommand, CommandError
from thyroid.models import Location

class Command(BaseCommand):
    help = 'Import latitude and longitude data from ThyroidMapLatLong.csv into the database'

    def handle(self, *args, **options):
        csv_file = 'ThyroidMapLatLong.csv'
        try:
            with open(csv_file, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    lat = row['LATNUM']
                    long = row['LONGNUM']
                    Location.objects.create(latnum=lat, longnum=long)
                self.stdout.write(self.style.SUCCESS('Successfully imported data'))
        except FileNotFoundError:
            raise CommandError(f'File "{csv_file}" does not exist')
        except KeyError:
            raise CommandError(f'CSV file must contain LATNUM and LONGNUM columns')
        except Exception as e:
            raise CommandError(f'An error occurred: {e}')

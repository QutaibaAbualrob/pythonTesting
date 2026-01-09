import csv
import os
from django.core.management.base import BaseCommand
from true_caller_app.models import Contact

class Command(BaseCommand):
    help = 'Load dummy data from CSV into Contact model'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **kwargs):
        csv_file_path = kwargs['csv_file']
        
        if not os.path.exists(csv_file_path):
            self.stdout.write(self.style.ERROR(f'File "{csv_file_path}" does not exist.'))
            return

        self.stdout.write(f"Loading data from {csv_file_path}...")

        with open(csv_file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            count = 0
            errors = 0
            
            for row in reader:
                try:
                    # Clean Boolean fields
                    is_spam_val = str(row.get('is_spam', 'False')).strip().lower() == 'true'
                    spam_score_val = int(row.get('spam_score', 0))
                    
                    # Create or Update based on phone_number
                    obj, created = Contact.objects.update_or_create(
                        phone_number=row['phone_number'].strip(),
                        defaults={
                            'name': row['name'],
                            'carrier': row['carrier'],
                            'is_spam': is_spam_val,
                            'spam_score': spam_score_val
                        }
                    )
                    
                    action = "Created" if created else "Updated"
                    self.stdout.write(self.style.SUCCESS(f"{action}: {row['phone_number']}"))
                    count += 1
                    
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error importing row {row}: {e}"))
                    errors += 1

        self.stdout.write(self.style.SUCCESS(f"\nSuccessfully loaded {count} contacts."))
        if errors > 0:
            self.stdout.write(self.style.WARNING(f"Encountered {errors} errors."))

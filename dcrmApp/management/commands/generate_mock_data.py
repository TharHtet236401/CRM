from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from dcrmApp.models import Record
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Generates mock data for testing'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='Number of records to create')

    def handle(self, *args, **kwargs):
        fake = Faker()
        count = kwargs['count']
        
        # Get all users or create a test user if none exists
        users = User.objects.all()
        if not users.exists():
            test_user = User.objects.create_user(
                username='testuser',
                password='testpass123'
            )
            users = [test_user]

        self.stdout.write('Creating mock records...')
        
        for i in range(count):
            # Generate a phone number in XXX-XXX-XXXX format (12 chars)
            phone = f"{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
            
            Record.objects.create(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.email(),
                phone=phone,
                address=fake.street_address(),
                city=fake.city(),
                state=fake.state(),
                zipcode=fake.zipcode(),
                added_by=random.choice(users)
            )
            
            if (i + 1) % 10 == 0:
                self.stdout.write(f'Created {i + 1} records...')
        
        self.stdout.write(self.style.SUCCESS(f'Successfully created {count} mock records')) 
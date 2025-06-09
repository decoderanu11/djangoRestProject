from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from customers.models import Customer
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Create sample customers for testing'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=10,
            help='Number of customers to create'
        )
    
    def handle(self, *args, **options):
        fake = Faker()
        count = options['count']
        
        # Create sample customers
        for i in range(count):
            customer = Customer.objects.create(
                name=fake.name(),
                email=fake.unique.email(),
                mobile=f"+{random.randint(1000000000, 9999999999)}",
                address=fake.address()
            )
            
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {count} sample customers')
        )
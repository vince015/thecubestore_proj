from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group


class Command(BaseCommand):

    def handle(self, *args, **options):
        if not Group.objects.filter(name='Staff').exists():
            Group.objects.create(name='Staff')

        if not Group.objects.filter(name='Merchant').exists():
            Group.objects.create(name='Merchant')
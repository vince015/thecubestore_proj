from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from django.contrib.contenttypes.models import ContentType


class Command(BaseCommand):

    def handle(self, *args, **options):

        if not Group.objects.filter(name='Staff').exists():
            group = Group.objects.create(name='Staff')
            group.permissions.add(contact_permission)

        if not Group.objects.filter(name='Merchant').exists():
            Group.objects.create(name='Merchant')

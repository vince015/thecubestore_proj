from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType


class Command(BaseCommand):

    def handle(self, *args, **options):
        contact_content_type = ContentType.objects.get(app_label='system_app',
                                                    model='Contact')
        contact_permission = Permission.objects.create(codename='contact_permission',
                                                       name='Can add, edit, delete contact',
                                                       content_type=contact_content_type)

        if not Group.objects.filter(name='Staff').exists():
            group = Group.objects.create(name='Staff')
            group.permissions.add(contact_permission)

        if not Group.objects.filter(name='Merchant').exists():
            Group.objects.create(name='Merchant')

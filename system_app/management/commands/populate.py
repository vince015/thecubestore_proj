from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group


class Command(BaseCommand):

    def handle(self, *args, **options):

        crew_group = Group.objects.get(name='Crew')

        # Create a new Crew
        if not User.objects.filter(username='j.delacruz').exists():
            crew = User.objects.create(username='j.delacruz',
                                     email='j.delacruz@cubestore.com.ph',
                                     first_name='Juan',
                                     last_name='dela Cruz')
            crew.set_password('pass1234')
            crew.groups.add(crew_group)
            crew.save()

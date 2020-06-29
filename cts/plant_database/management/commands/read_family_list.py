from django.core.management.base import BaseCommand, CommandError
from plant_database.models import Family


class Command(BaseCommand):
    help = 'Consumes a file containing one plant family name per line and creates ' \
           'a plant Family object from each'

    def add_arguments(self, parser):
        parser.add_argument('family_fpath', nargs='+', type=str)

    def handle(self, *args, **options):
        try:
            with open(options['family_fpath'][0], 'r') as f:
                for line in f:
                    family, created = Family.objects.get_or_create(name=line.strip())
                    if created:
                        family.save()
                        self.stdout.write(self.style.SUCCESS('Successfully created Family "%s"' % family))
        except FileNotFoundError as e:
            self.stdout.write(self.style.ERROR('[!] "%s"' % e))

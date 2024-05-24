import json
from django.core.management.base import BaseCommand
from backend.models import Indicator


class Command(BaseCommand):
    help = 'Insert indicators into the database from a JSON file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the JSON file containing indicators')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                indicators = json.load(file)

            for indicator in indicators:
                name = indicator.get('name')
                description = indicator.get('description')

                if not name or not description:
                    self.stdout.write(self.style.ERROR(f'Missing name or description for indicator: {indicator}'))
                    continue

                Indicator.objects.update_or_create(
                    name=name,
                    defaults={'description': description}
                )

            self.stdout.write(self.style.SUCCESS('Indicators inserted/updated successfully'))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'File not found: {file_path}'))
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR('Invalid JSON format'))


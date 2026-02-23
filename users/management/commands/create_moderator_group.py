# users/management/commands/create_moderator_group.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product
from django.conf import settings


class Command(BaseCommand):
    help = 'Создает группу модераторов и назначает права'

    def handle(self, *args, **options):
        # Создаем или получаем группу
        moderator_group, created = Group.objects.get_or_create(name='Модератор продуктов')

        if created:
            self.stdout.write(self.style.SUCCESS('Группа "Модератор продуктов" создана'))
        else:
            self.stdout.write(self.style.WARNING('Группа "Модератор продуктов" уже существует'))

        # Получаем content type для модели Product
        content_type = ContentType.objects.get_for_model(Product)

        # Создаем или получаем кастомные права
        can_unpublish, _ = Permission.objects.get_or_create(
            codename='can_unpublish_product',
            defaults={
                'name': 'Может отменять публикацию продукта',
                'content_type': content_type
            }
        )

        can_delete_any, _ = Permission.objects.get_or_create(
            codename='can_delete_any_product',
            defaults={
                'name': 'Может удалять любой продукт',
                'content_type': content_type
            }
        )

        # Получаем стандартное право на удаление
        try:
            delete_product = Permission.objects.get(
                codename='delete_product',
                content_type=content_type
            )
        except Permission.DoesNotExist:
            self.stdout.write(self.style.ERROR('Стандартное право delete_product не найдено'))
            self.stdout.write(self.style.WARNING('Выполните миграции: python manage.py migrate'))
            return

        # Добавляем права группе
        moderator_group.permissions.add(can_unpublish, can_delete_any, delete_product)

        self.stdout.write(
            self.style.SUCCESS('Права успешно назначены группе модераторов')
        )
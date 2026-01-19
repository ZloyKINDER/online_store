from django.db import models


class Blog(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовк", help_text="Введите заголовок статьи")
    content = models.TextField(
        verbose_name="Содержимое", blank=True, help_text="Введите текст статьи"
    )
    preview = models.ImageField(
        upload_to="image/blog/",
        blank=True,
        null=True,
        verbose_name="Превью",
        help_text="Загрузите изображение для превью"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    is_published = models.BooleanField(
        default=False,
        verbose_name="Опубликовано",
        help_text="Отметьте для публикации")
    views_count = models.PositiveIntegerField(
        default=0,
        verbose_name="Количество просмотров",
        editable=False
    )

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['created_at']

    def __str__(self):
        return self.title
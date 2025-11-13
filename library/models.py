from django.db import models
from django.utils import timezone

from users.models import User


class Author(models.Model):
    """Модель автора"""

    full_name = models.CharField(
        max_length=100,
        verbose_name="ФИО автора",
        help_text="Укажите ФИО автора",
        blank=False,  # Сделать обязательным
        null=False,
    )
    birth_date = models.DateField(
        verbose_name="Дата рождения",
        help_text="Укажите дату рождения",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"
        ordering = ["full_name"]

    def __str__(self):
        return self.full_name


class Book(models.Model):
    """Модель книги"""

    title = models.CharField(
        max_length=200,
        verbose_name="Название книги",
        help_text="Укажите название книги",
        blank=False,
        null=False,
    )
    description = models.TextField(
        verbose_name="Описание",
        help_text="Укажите описание книги",
        blank=True,
        null=True,
    )
    genre = models.CharField(
        max_length=100,
        verbose_name="Жанр",
        help_text="Укажите жанр",
        blank=True,
        null=True,
    )
    authors = models.ManyToManyField(
        Author,
        verbose_name="Авторы",
        help_text="Выберите одного или нескольких авторов",
    )
    publication_date = models.DateField(
        verbose_name="Дата публикации",
        help_text="Укажите дату публикации",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"
        ordering = ["title"]

    def __str__(self):
        return self.title

    def get_authors_names(self):
        """Получить имена авторов через запятую"""
        return ", ".join([author.full_name for author in self.authors.all()])


class Issuance(models.Model):
    """Модель выдачи книги"""

    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, verbose_name="Книга", help_text="Выберите книгу"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        help_text="Выберите пользователя",
    )
    issue_date = models.DateField(default=timezone.now, verbose_name="Дата выдачи")
    return_date = models.DateField(null=True, blank=True, verbose_name="Дата возврата")

    class Meta:
        verbose_name = "Выдача"
        verbose_name_plural = "Выдачи"
        ordering = ["-issue_date"]

    def __str__(self):
        return f"{self.book.title} - {self.user.username}"

    def is_returned(self):
        """Проверка, возвращена ли книга"""
        return self.return_date is not None

    def days_overdue(self):
        """Расчет дней просрочки (если больше 30 дней)"""
        if not self.is_returned():
            days = (timezone.now().date() - self.issue_date).days
            return max(0, days - 30)
        return 0

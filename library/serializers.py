from django.utils import timezone
from rest_framework import serializers

from .models import Author, Book, Issuance


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"

    def validate_full_name(self, value):
        if len(value.strip()) < 2:
            raise serializers.ValidationError(
                "ФИО автора должно содержать минимум 2 символа"
            )
        return value.strip()

    def validate_birth_date(self, value):
        if value and value > timezone.now().date():
            raise serializers.ValidationError("Дата рождения не может быть в будущем")
        return value


class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True, read_only=True)
    authors_names = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = "__all__"

    def get_authors_names(self, obj):
        return obj.get_authors_names()

    def validate_title(self, value):
        if len(value.strip()) < 2:
            raise serializers.ValidationError(
                "Название книги должно содержать минимум 2 символа"
            )
        return value.strip()

    def validate_publication_date(self, value):
        if value and value > timezone.now().date():
            raise serializers.ValidationError("Дата публикации не может быть в будущем")
        return value


class IssuanceSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source="book.title", read_only=True)
    user_email = serializers.CharField(source="user.email", read_only=True)
    is_returned = serializers.BooleanField(read_only=True)
    days_overdue = serializers.IntegerField(read_only=True)

    class Meta:
        model = Issuance
        fields = "__all__"
        read_only_fields = ("issue_date",)

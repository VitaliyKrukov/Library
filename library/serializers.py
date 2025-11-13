from rest_framework import serializers

from .models import Author, Book, Issuance


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"


class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True, read_only=True)
    authors_names = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = "__all__"

    def get_authors_names(self, obj):
        return obj.get_authors_names()


class IssuanceSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source="book.title", read_only=True)
    user_username = serializers.CharField(source="users.username", read_only=True)
    is_returned = serializers.BooleanField(read_only=True)
    days_overdue = serializers.IntegerField(read_only=True)

    class Meta:
        model = Issuance
        fields = "__all__"
        read_only_fields = ("issue_date",)

from django.contrib import admin

from .models import Author, Book, Issuance


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("full_name", "birth_date")
    search_fields = ("full_name",)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "genre", "publication_date")
    search_fields = ("title", "genre")
    filter_horizontal = ("authors",)


@admin.register(Issuance)
class IssuanceAdmin(admin.ModelAdmin):
    list_display = ("book", "user", "issue_date", "return_date")
    list_filter = ("issue_date", "return_date")
    search_fields = ("book__title", "user__username")

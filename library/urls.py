from django.urls import path

from . import views

urlpatterns = [
    path("authors/", views.AuthorListCreateView.as_view(), name="author-list"),
    path("authors/<int:pk>/", views.AuthorDetailView.as_view(), name="author-detail"),
    path("books/", views.BookListCreateView.as_view(), name="book-list"),
    path("books/<int:pk>/", views.BookDetailView.as_view(), name="book-detail"),
    path("issuances/", views.IssuanceListCreateView.as_view(), name="issuance-list"),
    path(
        "issuances/<int:pk>/",
        views.IssuanceDetailView.as_view(),
        name="issuance-detail",
    ),
    path("issuances/<int:pk>/return/", views.return_book, name="return-book"),
    path("issuances/my/", views.user_issuances, name="my-issuances"),
]

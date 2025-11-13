from django.utils import timezone
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Author, Book, Issuance
from .serializers import AuthorSerializer, BookSerializer, IssuanceSerializer


class AuthorListCreateView(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated]


class AuthorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated]


class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Book.objects.all()
        search = self.request.query_params.get("search")

        if search:
            queryset = queryset.filter(title__icontains=search)

        return queryset


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


class IssuanceListCreateView(generics.ListCreateAPIView):
    serializer_class = IssuanceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Issuance.objects.all()
        return Issuance.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(issue_date=timezone.now().date())


class IssuanceDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = IssuanceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Issuance.objects.all()
        return Issuance.objects.filter(user=user)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def return_book(request, pk):
    try:
        issuance = Issuance.objects.get(pk=pk)

        if issuance.user != request.user and not request.user.is_staff:
            return Response(
                {"error": "Нет прав для выполнения операции"},
                status=status.HTTP_403_FORBIDDEN,
            )

        if issuance.return_date:
            return Response(
                {"error": "Книга уже возвращена"}, status=status.HTTP_400_BAD_REQUEST
            )

        issuance.return_date = timezone.now().date()
        issuance.save()

        serializer = IssuanceSerializer(issuance)
        return Response(serializer.data)

    except Issuance.DoesNotExist:
        return Response(
            {"error": "Выдача не найдена"}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_issuances(request):
    issuances = Issuance.objects.filter(user=request.user)
    serializer = IssuanceSerializer(issuances, many=True)
    return Response(serializer.data)

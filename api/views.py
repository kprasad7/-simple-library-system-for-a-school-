from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Q

from .models import Book, BorrowedBook, Student
from .serializers import BookSerializer, BorrowedBookSerializer


class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookDetail(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BorrowedBookList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        student = get_object_or_404(Student, pk=pk)
        borrowed_books = BorrowedBook.objects.filter(student=student)
        serializer = BorrowedBookSerializer(borrowed_books, many=True)
        return Response(serializer.data)

    def post(self, request, pk, book_id):
        student = get_object_or_404(Student, pk=pk)
        book = get_object_or_404(Book, pk=book_id)

        # Check if the student has already borrowed the book
        if BorrowedBook.objects.filter(student=student, book=book, returned_date=None).exists():
            return Response({'error': 'You have already borrowed this book.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the book is available
        if book.available_copies <= 0:
            return Response({'error': 'This book is currently unavailable.'}, status=status.HTTP_400_BAD_REQUEST)

        # Register the borrowed book
        borrowed_book = BorrowedBook.objects.create(student=student, book=book, borrowed_date=timezone.now(),due_date=timezone.now() + timezone.timedelta(days=14))
        borrowed_book.save()

        # Update the available copies of the book
        book.available_copies -= 1
        book.save()

        return Response({'success': 'Book borrowed successfully.'}, status=status.HTTP_201_CREATED)

    def put(self, request, pk, book_id):
        student = get_object_or_404(Student, pk=pk)
        borrowed_book = get_object_or_404(BorrowedBook, student=student, book__id=book_id, returned_date=None)

        # Check if the book can be renewed
        if borrowed_book.renewed_date is not None:
            return Response({'error': 'This book has already been renewed.'}, status=status.HTTP_400_BAD_REQUEST)

        # Renew the borrowed book
        borrowed_book.due_date += timezone.timedelta(days=14)
        borrowed_book.renewed_date = timezone.now()
        borrowed_book.save()

        return Response({'success': 'Book renewed successfully.'}, status=status.HTTP_200_OK)

    def delete(self, request, pk, book_id):
        student = get_object_or_404(Student, pk=pk)
        borrowed_book = get_object_or_404(BorrowedBook, student=student, book__id=book_id, returned_date=None)

        # Return the borrowed book
        borrowed_book.returned_date = timezone.now()
        borrowed_book.save()

        # Update the available copies of the book
        book = borrowed_book.book
        book.available_copies += 1
        book.save()

        return Response({'success': 'Book returned successfully.'}, status=status.HTTP_200_OK)



class BorrowedBookHistory(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        student = get_object_or_404(Student, pk=pk)
        borrowed_books = BorrowedBook.objects.filter(student=student, returned_date__isnull=False)
        serializer = BorrowedBookSerializer(borrowed_books, many=True)
        return Response(serializer.data)

from rest_framework import serializers
from .models import Book, Student, BorrowedBook

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'isbn', 'description', 'num_copies', 'available_copies']

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'name', 'email', 'password']

class BorrowedBookSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    student = StudentSerializer(read_only=True)

    class Meta:
        model = BorrowedBook
        fields = ['id', 'book', 'student', 'borrowed_date', 'due_date', 'renewed_date', 'returned_date']

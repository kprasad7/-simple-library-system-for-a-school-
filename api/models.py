
from django.db import models
from django.utils import timezone


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    isbn = models.CharField(max_length=20)
    description = models.TextField()
    num_copies = models.IntegerField()
    available_copies = models.IntegerField(default=num_copies)

    def __str__(self):
        return self.title


class Student(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    password = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class BorrowedBook(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    borrowed_date = models.DateField(default=timezone.now)
    due_date = models.DateField()
    renewed_date = models.DateField(null=True, blank=True)
    returned_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.name} borrowed {self.book.title}"

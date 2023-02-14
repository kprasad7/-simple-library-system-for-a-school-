define the following URL patterns:


/books/: This maps to the BookList view, which lists all the books in the library.

/books/<int:pk>/: This maps to the BookDetail view, which shows the details of a specific book.

/students/<int:pk>/borrowed-books/: This maps to the BorrowedBookList view, which lists the borrowed books of a specific student. The pk parameter is the primary key of the student.

/students/<int:pk>/borrowed-books/<int:book_id>/: This maps to the BorrowedBookList view, which allows a student to borrow, renew or return a specific book. The pk parameter is the primary key of the student, and book_id is the primary key of the book.

/students/<int:pk>/borrowed-books/<int:book_id>/renew/: This maps to the BorrowedBookList view, which allows a student to renew a specific borrowed book. The pk parameter is the primary key of the student, and book_id is the primary key of the book.


/students/<int:pk>/borrowed-books/<int:book_id>/return/: This maps to the BorrowedBookList view, which allows a student to return a specific borrowed book. The pk parameter is the primary key of the student, and book_id is the primary key of the book.

/students/<int:pk>/borrowed-books/history/: This maps to the BorrowedBookHistory view, which shows the borrowing history of a specific student. The pk parameter is the primary key of the student.

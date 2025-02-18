from django.urls import path
from . import views

# Khai báo view tương ứng với url
urlpatterns = [
    path("", views.index, name="index"),
    path("books/", views.BookListView.as_view(), name="books"),
    path("book/<int:pk>", views.BookDetailView.as_view(), name="book-detail"),
    path("mybooks/", views.LoanedBooksByUserListView.as_view(), name="my-borrowed"),
]

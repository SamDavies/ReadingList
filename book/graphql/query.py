from graphene import List, String
from book.graphql.fields import BookField, AuthorField

from book.fetcher import sort_by, get_book_data, group_by_author


class BookQuery:
    books = List(BookField, order_by=String())
    authors = List(AuthorField)

    def resolve_books(self, _, order_by):
        books = get_book_data()
        sorted_books = sort_by(key=order_by, books=books)
        return [BookField(
            book_id=book["book_id"],
            name=book["name"],
            isbn=book["isbn"],
            published_at=book["published_at"],
            author=book["author"],
            cover=book["cover"],
        ) for book in sorted_books]

    def resolve_authors(self, _):
        books = get_book_data()
        return [AuthorField(
            name=author["name"],
            books=[BookField(
                book_id=book["book_id"],
                name=book["name"],
                isbn=book["isbn"],
                published_at=book["published_at"],
                author=book["author"],
                cover=book["cover"],
            ) for book in author["books"]]
        ) for author in group_by_author(books)]

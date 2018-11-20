from graphene import List, String
from book.graphql.fields import BookField, AuthorField

from book.fetcher import sort_by, get_book_data, group_by_author


class BookQuery:
    books = List(BookField, order_by=String())
    authors = List(AuthorField)

    def resolve_books(self, _, order_by):
        books = get_book_data()
        return sort_by(key=order_by, books=books)

    def resolve_authora(self, _):
        books = get_book_data()
        return group_by_author(books)

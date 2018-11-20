from flask_restful import Resource

from book.fetcher import sort_by, get_book_data, group_by_author


class Books(Resource):
    def get(self):
        return get_book_data()


class BooksSorted(Resource):
    def get(self, order_by):
        books = get_book_data()
        return sort_by(key=order_by, books=books)


class Authors(Resource):
    def get(self):
        books = get_book_data()
        return group_by_author(books)

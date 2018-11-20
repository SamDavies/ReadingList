from flask import Blueprint
from flask_restful import Api

from book.rest.api import Books, BooksSorted, Authors

books = Blueprint('books', __name__, url_prefix='/books')
api = Api(books)

api.add_resource(Books, '')
api.add_resource(Authors, '/authors')
api.add_resource(BooksSorted, '/<order_by>')

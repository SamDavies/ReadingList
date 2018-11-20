from graphene import ObjectType, String, Int, List


class BookField(ObjectType):
    book_id = Int()
    name = String()
    isbn = String()
    published_at = String()
    author = String()
    cover = String()


class AuthorField(ObjectType):
    name = String()
    books = List(BookField)

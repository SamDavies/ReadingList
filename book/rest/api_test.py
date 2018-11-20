from app import create_app


class TestBookAPI:
    def test_books(self):
        # When
        client = create_app().test_client()

        response = client.get('/books')

        # Then
        assert response.json[0]['book_id'] == 1

    def test_books_order_by(self):
        # When
        client = create_app().test_client()

        response = client.get('/books/-name')

        # Then
        assert response.json[-1]['book_id'] == 1

    def test_authors(self):
        # When
        client = create_app().test_client()

        response = client.get('/books/authors')

        # Then
        assert response.json[0]['books'][0]['book_id'] == 1

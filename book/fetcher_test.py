from book.fetcher import get_book_data, sort_by


def test_get_book_data():
    assert len(get_book_data()) > 0


def test_sort_by_published_at_ascending():
    # Given
    books = [
        {"book_id": 1, "published_at": "2000-01-01"},
        {"book_id": 2, "published_at": "1991-07-29"},
    ]

    # When
    sorted_books = sort_by("published_at", books)

    # Then
    assert sorted_books[0]["book_id"] == 2
    assert sorted_books[1]["book_id"] == 1


def test_sort_by_published_at_descending():
    # Given
    books = [
        {"book_id": 2, "published_at": "1991-07-29"},
        {"book_id": 1, "published_at": "2000-01-01"},
    ]

    # When
    sorted_books = sort_by("-published_at", books)

    # Then
    assert sorted_books[0]["book_id"] == 1
    assert sorted_books[1]["book_id"] == 2


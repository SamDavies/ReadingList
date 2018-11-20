from book.fetcher import get_book_data, sort_by, group_by_author


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


def test_sort_by_name_ascending():
    # Given
    books = [
        {"book_id": 1, "name": "b"},
        {"book_id": 2, "name": "a"},
    ]

    # When
    sorted_books = sort_by("name", books)

    # Then
    assert sorted_books[0]["book_id"] == 2
    assert sorted_books[1]["book_id"] == 1


def test_sort_by_name_descending():
    # Given
    books = [
        {"book_id": 2, "name": "a"},
        {"book_id": 1, "name": "b"},
    ]

    # When
    sorted_books = sort_by("-name", books)

    # Then
    assert sorted_books[0]["book_id"] == 1
    assert sorted_books[1]["book_id"] == 2


def test_group_by_author():
    # Given
    books = [
        {"book_id": 2, "author": "a"},
        {"book_id": 1, "author": "b"},
        {"book_id": 3, "author": "b"},
    ]

    # When
    authors = group_by_author(books)

    # Then
    expected = [{
        "name": "a",
        "books": [
            {"book_id": 2, "author": "a"},
        ]
    }, {
        "name": "b",
        "books": [
            {"book_id": 1, "author": "b"},
            {"book_id": 3, "author": "b"},
        ]
    }]
    assert authors == expected

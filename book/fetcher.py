from datetime import datetime

import requests

ENDPOINT = "https://s3-eu-west-1.amazonaws.com/styl-reading-list/data.json"


def get_book_data():
    return requests.get(ENDPOINT).json()["books"]


def sort_by(key, books):
    reverse = True if key[0] == "-" else False
    key = key if key[0] != "-" else key[1:]

    if key == "published_at":
        return sorted(books, key=lambda book: datetime.strptime(book[key], "%Y-%m-%d"), reverse=reverse)

    if key == "name":
        return sorted(books, key=lambda book: book[key], reverse=reverse)

    return books


def group_by_author(books):
    authors = []
    for book in books:

        def append_book():
            # Add this book to an existing author if they exist
            for author in authors:
                if author["name"] == book["author"]:
                    author["books"].append(book)
                    return

            # append a new author to the list
            authors.append({
                "name": book["author"],
                "books": [book]
            })

        append_book()

    return authors

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
    return books

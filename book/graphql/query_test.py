from graphene.test import Client

from core.schema import schema


class TestBookQuery:
    def test_resolve_books(self):
        # When
        client = Client(schema)

        query = """
            {{
                books(orderBy: "{order_by}") {{
                    bookId
                }}
            }}
        """.format(order_by="name")
        response = client.execute(query)

        # Then
        assert response['data']['books'][0]['bookId'] == 1

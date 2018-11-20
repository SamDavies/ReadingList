import graphene

from book.graphql.query import BookQuery


class Query(
    BookQuery,
    graphene.ObjectType
):
    # This class will inherit from multiple Queries
    pass


schema = graphene.Schema(
    query=Query,
    mutation=None,
)

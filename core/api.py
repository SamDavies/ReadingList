from flask import Blueprint
from flask_graphql import GraphQLView

from core.schema import schema

graphql_api = Blueprint('graphql', __name__, url_prefix='')

graphql_api.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True,
    )
)

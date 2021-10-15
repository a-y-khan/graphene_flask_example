from flask import Flask, redirect, url_for
from flask_graphql import GraphQLView
from example.database import db_session, init_db
from example.schema import schema

app = Flask(__name__)

app.add_url_rule(
    '/graphql', view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True,
        context={'session': db_session},
    ))


@app.route('/')
def index():
    #return "GraphQL at /graphql"
    return redirect(url_for('graphql'))


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if '__main__' == __name__:
    # for testing purposes
    init_db()
    app.run(host='0.0.0.0', port=5001, debug=True)

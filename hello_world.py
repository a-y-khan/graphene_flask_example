import graphene as gp

class Query(gp.ObjectType):
    hello = gp.String(argument=gp.String(default_value='world'))

    # this is where the magic happens!
    # pattern is always resolve_<field>
    def resolve_hello(self, info, argument):
        # info: ResolveInfo (https://github.com/graphql-python/graphql-core)
        return 'hello ' + argument
schema = gp.Schema(query=Query)

if '__main__' == __name__:
    # GraphQL's default serialization format is JSON!
    query = """
    {
        hello
    }
    """
    query_with_argument = """
    {
        hello(argument: "universe!")
    }
    """
    # result is OrderedDict
    result = schema.execute(query)
    print(result.data['hello'])
    result = schema.execute(query_with_argument)
    print(result.data['hello'])
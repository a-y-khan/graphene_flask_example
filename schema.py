import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType, utils
from models import House as HouseModel


class House(SQLAlchemyObjectType):
	class Meta:
		model = HouseModel
		interfaces = (relay.Node, )


class HouseConnetion(relay.Connection):
	class Meta:
		node = House


class Query(graphene.ObjectType):
	node = relay.Node.Field()
	
	# set sort=None argument to disable ability to sort
	# all_houses = SQLAlchemyConnectionField(HouseConnetion, sort=None)
	all_houses = SQLAlchemyConnectionField(HouseConnetion)


schema = graphene.Schema(query=Query, types=[House])

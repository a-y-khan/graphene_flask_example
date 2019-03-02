import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType, utils
from models import House as HouseModel
from models import Student as StudentModel
from models import Pet as PetModel


class House(SQLAlchemyObjectType):
	class Meta:
		model = HouseModel
		interfaces = (relay.Node, )


class HouseConnetion(relay.Connection):
	class Meta:
		node = House


class Student(SQLAlchemyObjectType):
	class Meta:
		model = StudentModel
		interfaces = (relay.Node, )


class StudentConnection(relay.Connection):
	class Meta:
		node = Student


class Pet(SQLAlchemyObjectType):
	class Meta:
		model = PetModel
		interfaces = (relay.Node, )


class PetConnection(relay.Connection):
	class Meta:
		node = Pet


# TODO: more sorts and queries!

class Query(graphene.ObjectType):
	node = relay.Node.Field()
	
	# set sort=None argument to disable ability to sort
	# all_houses = SQLAlchemyConnectionField(HouseConnetion, sort=None)
	all_houses = SQLAlchemyConnectionField(HouseConnetion)
	all_students = SQLAlchemyConnectionField(StudentConnection)
	all_pets = SQLAlchemyConnectionField(PetConnection)


schema = graphene.Schema(query=Query, types=[House, Student, Pet])
